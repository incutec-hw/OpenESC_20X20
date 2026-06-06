#!/usr/bin/env python3
"""
4in1 ESC Power Loss & Thermal Calculator

Models AM32 trapezoidal 6-step commutation with steady-state and transient thermal.
Supports both 20x20 and 30x30 ESC variants with datasheet-verified parameters.

Datasheets:
  20x20: SP40N03GNJ (Siliup Ver-1.2) + NSG2065Q (NSIC V1.0), Rg=15Ω
  30x30: SP40N01GHNK (Siliup Ver-1.1) + NSG2065Q (NSIC V1.0), Rg=8Ω
"""

import argparse
import math

# ═══════════════════════════════════════════════════════════════
#  MOSFET profiles — all values from datasheets
# ═══════════════════════════════════════════════════════════════

PROFILES = {
    "20x20": {
        "name":         "20×20  SP40N03GNJ (3×3mm)",
        # ── SP40N03GNJ datasheet (Ver-1.2) ──
        "rds_on":       2.9e-3,     # Ω typ @ Vgs=10V, ID=20A, 25°C
        "rds_on_max":   3.7e-3,     # Ω max
        "rds_tempco":   1.45,       # normalized @ 100°C (p3 curve)
        "rds_tempco_150": 1.70,     # normalized @ 150°C
        "qg_at_10v":    15e-9,      # C  (from gate charge curve p3 @ Vgs=10V)
        "qgd":          5.5e-9,     # C  gate-drain (Miller) charge
        "vgs":          10.0,       # V
        "rg":           15.0,       # Ω  external gate resistor
        "v_plateau":    3.0,        # V  Miller plateau (transfer curve p3)
        # Switching: Qgd / I_gate through Rg
        #   I_on  = (10-3)/15 = 0.47A → tr = 5.5nC/0.47A = 11.7ns
        #   I_off = 3/15      = 0.20A → tf = 5.5nC/0.20A = 27.5ns
        "tr":           11.7e-9,
        "tf":           27.5e-9,
        "vf_body_cold": 0.80,       # V  @ ~30A, 25°C (p4 curve extrapolated)
        "vf_body_hot":  0.65,       # V  @ ~30A, 100°C
        "trr":          14e-9,      # s  (p2)
        "qrr":          23e-9,      # C  (p2)
        "rth_jc":       2.27,       # °C/W (p2)
        "pd_max":       55.0,       # W
        "tj_max":       150.0,      # °C
        # Board
        "board_mm":     20,         # mm mounting pattern
        "board_area":   1030.0,     # mm² actual PCB (~31×33mm, from Edge.Cuts)
        "r_copper":     3.2e-3,     # Ω per phase trace
        "r_shunt":      0.2e-3,     # Ω
        "layers":       6,
        "oz_outer":     1,          # oz copper
        "oz_inner":     0.5,
    },
    "30x30": {
        "name":         "30×30  SP40N01GHNK (5×6mm)",
        # ── SP40N01GHNK datasheet (Ver-1.1) ──
        "rds_on":       1.2e-3,     # Ω typ @ Vgs=10V, ID=20A, 25°C
        "rds_on_max":   1.5e-3,     # Ω max
        "rds_tempco":   1.45,       # normalized @ 100°C (p3 curve)
        "rds_tempco_150": 1.70,     # normalized @ 150°C
        "qg_at_10v":    65e-9,      # C  (from gate charge curve p3 @ Vgs=10V)
        "qgd":          15.5e-9,    # C  gate-drain (Miller) charge
        "vgs":          10.0,       # V
        "rg":           8.0,        # Ω  external gate resistor
        "v_plateau":    3.5,        # V  Miller plateau (transfer curve p3, higher Vth)
        # Switching: Qgd / I_gate through Rg
        #   I_on  = (10-3.5)/8 = 0.81A → tr = 15.5nC/0.81A = 19.1ns
        #   I_off = 3.5/8      = 0.44A → tf = 15.5nC/0.44A = 35.2ns
        "tr":           19.1e-9,
        "tf":           35.2e-9,
        "vf_body_cold": 0.75,       # V  @ ~30A, 25°C (p3 source-drain diode curve)
        "vf_body_hot":  0.60,       # V  @ ~30A, 100°C
        "trr":          29e-9,      # s  (p2)
        "qrr":          113e-9,     # C  (p2) — much higher than SP40N03GNJ
        "rth_jc":       0.96,       # °C/W (p2) — better, larger package
        "pd_max":       130.0,      # W
        "tj_max":       150.0,      # °C
        # Board
        "board_mm":     30,         # mm mounting pattern
        "board_area":   1770.0,     # mm² actual PCB (~42×43mm, from Edge.Cuts)
        "r_copper":     2.0e-3,     # Ω per phase (wider traces, more area)
        "r_shunt":      0.2e-3,     # Ω
        "layers":       6,
        "oz_outer":     1,
        "oz_inner":     0.5,
    },
}

# ─── NSG2065Q gate driver (shared) ───
GATE_DRIVER = {
    "dead_time_typ":  200e-9,   # s  hardware dead time (100-300ns, p6)
    "dead_time_min":  100e-9,
    "dead_time_max":  300e-9,
    "io_source":      1.2,      # A
    "io_sink":        1.5,      # A
}

# ─── Thermal scenarios ───
# h = convective heat transfer coefficient (W/m²·K)
# θ_board = 1 / (h × A_both_sides)
THERMAL_SCENARIOS = {
    "still":        {"h": 15,   "label": "Still air (bench)"},
    "light_flow":   {"h": 50,   "label": "Light prop wash (~3m/s)"},
    "strong_flow":  {"h": 100,  "label": "Strong prop wash (~8m/s)"},
    "direct_blast": {"h": 150,  "label": "Direct motor blast (>10m/s)"},
}

# ─── PCB stackup options for thermal comparison ───
# Copper thickness: 1oz=35µm, 2oz=70µm, 0.5oz=17.5µm
# Thermal conductivity: Cu=385 W/(m·K), FR4=0.3 W/(m·K)
PCB_OPTIONS = {
    "jlcpcb_6L_1oz": {
        "label":    "JLCPCB 6L 1oz/0.5oz (current)",
        "oz_outer": 1.0, "oz_inner": 0.5, "layers": 6,
        "notes":    "Standard, free POFV via-in-pad",
    },
    "jlcpcb_6L_2oz": {
        "label":    "JLCPCB 6L 2oz/2oz (max multilayer)",
        "oz_outer": 2.0, "oz_inner": 2.0, "layers": 6,
        "notes":    "Max Cu at JLCPCB for 6L, ~2x bare board cost",
    },
    "jlcpcb_4L_2oz": {
        "label":    "JLCPCB 4L 2oz/2oz",
        "oz_outer": 2.0, "oz_inner": 2.0, "layers": 4,
        "notes":    "Cheaper than 6L, no free POFV",
    },
    "jlcpcb_6L_3oz": {
        "label":    "JLCPCB 6L 3oz/1oz (industry std ESC)",
        "oz_outer": 3.0, "oz_inner": 1.0, "layers": 6,
        "notes":    "What commercial 35A ESCs use",
    },
    "pcbway_6L_4oz": {
        "label":    "PCBWay 6L 4oz/2oz (heavy Cu)",
        "oz_outer": 4.0, "oz_inner": 2.0, "layers": 6,
        "notes":    "PCBWay supports >2oz on multilayer, premium cost",
    },
}


def board_theta(area_mm2: float, h: float) -> float:
    """Board-to-ambient thermal resistance (°C/W), both sides convecting."""
    area_m2 = area_mm2 * 2.0 * 1e-6
    return 1.0 / (h * area_m2)


def board_thermal_mass(area_mm2: float, layers: int, oz_outer: float, oz_inner: float,
                       board_thickness_mm: float = 1.6) -> float:
    """Board thermal capacitance in J/K.

    Accounts for FR-4 substrate and copper layers.
    FR-4: ρ=1.85 g/cm³, cp=1.1 J/(g·K)
    Cu:   ρ=8.96 g/cm³, cp=0.385 J/(g·K)
    """
    area_cm2 = area_mm2 * 1e-2  # mm² → cm²

    # FR-4 volume (approximate: total thickness minus copper)
    cu_outer_mm = oz_outer * 0.035  # mm per oz
    cu_inner_mm = oz_inner * 0.035 if oz_inner else 0.0175
    n_inner = max(layers - 2, 0)
    total_cu_mm = 2 * cu_outer_mm + n_inner * cu_inner_mm
    fr4_mm = board_thickness_mm - total_cu_mm
    fr4_vol_cm3 = area_cm2 * fr4_mm * 0.1  # cm²×mm→cm³ needs ×0.1
    fr4_mass = fr4_vol_cm3 * 1.85
    fr4_cth = fr4_mass * 1.1

    # Copper volume
    cu_vol_cm3 = area_cm2 * total_cu_mm * 0.1
    cu_mass = cu_vol_cm3 * 8.96
    cu_cth = cu_mass * 0.385

    return fr4_cth + cu_cth


def copper_resistance_scaled(r_base: float, oz_base: float, oz_new: float) -> float:
    """Scale copper trace resistance for different copper weight.
    R ∝ 1/thickness, so doubling oz halves resistance.
    """
    return r_base * oz_base / oz_new


def calc_phase_losses(i: float, v_bus: float, duty: float, f_pwm: float,
                      comp_pwm: bool, dead_time: float, p: dict,
                      r_copper_override: float = None) -> dict:
    """Calculate losses for one active phase pair."""
    rds = p["rds_on"] * p["rds_tempco"]  # hot Rds(on)
    vf = p["vf_body_hot"]
    r_cu = r_copper_override if r_copper_override else p["r_copper"]

    # Conduction
    p_cond_hs = i**2 * rds * duty
    if comp_pwm:
        p_cond_ls = i**2 * rds * (1.0 - duty)
        p_body = 0.0
    else:
        p_cond_ls = 0.0
        p_body = vf * i * (1.0 - duty)
    p_cond_low = i**2 * rds  # LOW-phase FET, 100% on

    # Switching (Miller plateau crossing)
    p_switch = 0.5 * v_bus * i * (p["tr"] + p["tf"]) * f_pwm

    # Dead time (both edges per PWM cycle)
    p_dead = vf * i * dead_time * 2.0 * f_pwm

    # Reverse recovery (Qrr-based model)
    p_rr = p["qrr"] * v_bus * f_pwm

    # Gate drive (HS at f_pwm, LS at commutation freq ~200Hz)
    p_gate = p["qg_at_10v"] * p["vgs"] * f_pwm + p["qg_at_10v"] * p["vgs"] * 200

    # Copper (both phase traces in the current path)
    p_copper = i**2 * r_cu * 2.0

    # Shunt
    p_shunt = i**2 * p["r_shunt"]

    p_fet = p_cond_hs + p_cond_ls + p_body + p_cond_low + p_switch + p_dead + p_rr + p_gate
    p_passive = p_copper + p_shunt
    p_total = p_fet + p_passive

    return {
        "p_cond_hs": p_cond_hs, "p_cond_ls": p_cond_ls, "p_body": p_body,
        "p_cond_low": p_cond_low, "p_switch": p_switch, "p_dead": p_dead,
        "p_rr": p_rr, "p_gate": p_gate, "p_copper": p_copper, "p_shunt": p_shunt,
        "p_fet": p_fet, "p_passive": p_passive, "p_total": p_total,
    }


def transient_time_to_tj(p_board: float, theta_ba: float, c_th: float,
                         tj_max: float, t_ambient: float) -> float:
    """Time (seconds) from ambient to Tj_max under constant power.

    Simple first-order RC model: ΔT(t) = ΔT_ss × (1 - e^(-t/τ))
    τ = C_th × θ_ba
    Returns float('inf') if steady-state ΔT < (Tj_max - T_ambient).
    """
    dt_max = tj_max - t_ambient
    dt_ss = p_board * theta_ba
    if dt_ss <= dt_max:
        return float('inf')  # never reaches Tj_max
    tau = c_th * theta_ba
    return -tau * math.log(1.0 - dt_max / dt_ss)


def print_full_report(profile_key: str, i: float, v_bus: float, duty: float,
                      f_pwm: float, comp_pwm: bool, dead_time: float, n_active: int):
    p = PROFILES[profile_key]
    rds_hot = p["rds_on"] * p["rds_tempco"]
    losses = calc_phase_losses(i, v_bus, duty, f_pwm, comp_pwm, dead_time, p)

    p_board = losses["p_total"] * n_active
    p_motor = v_bus * i * duty * n_active
    eff = p_motor / (p_motor + p_board) * 100 if p_motor > 0 else 0

    print("=" * 70)
    print(f"  4in1 ESC Power Loss Report  —  {p['name']}")
    print(f"  AM32 6-Step Trapezoidal  |  NSG2065Q gate driver")
    print("=" * 70)
    print(f"  Battery voltage:      {v_bus:.1f} V")
    print(f"  Phase current:        {i:.1f} A")
    print(f"  Duty cycle:           {duty*100:.1f}%")
    print(f"  PWM frequency:        {f_pwm/1e3:.0f} kHz")
    print(f"  Dead time:            {dead_time*1e9:.0f} ns  (NSG2065Q HW)")
    print(f"  Comp PWM:             {'ON' if comp_pwm else 'OFF'}")
    print(f"  Gate resistor:        {p['rg']:.0f}Ω  →  tr={p['tr']*1e9:.1f}ns  tf={p['tf']*1e9:.1f}ns")
    print(f"  Rds(on):              {p['rds_on']*1e3:.1f}mΩ cold → {rds_hot*1e3:.1f}mΩ hot (×{p['rds_tempco']})")
    print(f"  Active phases:        {n_active}")
    print("-" * 70)

    print(f"\n  Per phase pair (HS + LS MOSFET + copper):")
    print(f"    HS conduction:     {losses['p_cond_hs']:7.3f} W  (I²×Rds×D)")
    if comp_pwm:
        print(f"    LS sync rect:      {losses['p_cond_ls']:7.3f} W  (I²×Rds×(1-D))")
    else:
        print(f"    Body diode:        {losses['p_body']:7.3f} W  (Vf×I×(1-D))")
    print(f"    LOW-phase FET:     {losses['p_cond_low']:7.3f} W  (I²×Rds, 100%)")
    print(f"    Switching:         {losses['p_switch']:7.3f} W")
    print(f"    Dead time:         {losses['p_dead']:7.3f} W")
    print(f"    Reverse recovery:  {losses['p_rr']:7.3f} W  (Qrr={p['qrr']*1e9:.0f}nC)")
    print(f"    Gate drive:        {losses['p_gate']:7.3f} W")
    print(f"    ────────────────────────────────────────")
    print(f"    FET subtotal:      {losses['p_fet']:7.3f} W")
    print(f"    Copper (×2):       {losses['p_copper']:7.3f} W  ({p['r_copper']*1e3:.1f}mΩ/phase)")
    print(f"    Shunt:             {losses['p_shunt']:7.3f} W")
    print(f"    ────────────────────────────────────────")
    print(f"    Phase total:       {losses['p_total']:7.3f} W")

    print(f"\n  Board totals ({n_active} phases):")
    print(f"    Heat dissipation:  {p_board:7.2f} W")
    print(f"    Motor output:      {p_motor:7.1f} W")
    print(f"    Efficiency:        {eff:7.1f}%")

    # ─── Steady-state thermal ───
    area = p["board_area"]
    c_th = board_thermal_mass(area, p["layers"], p["oz_outer"], p["oz_inner"])

    print(f"\n  Steady-state thermal ({area:.0f}mm² board, {p['layers']}L "
          f"{p['oz_outer']:.0f}oz/{p['oz_inner']}oz):")
    print(f"  {'Scenario':<28s} {'θ':>6s}  {'ΔT':>6s}  {'Tj@25°C':>7s}  {'Tj@40°C':>7s}")
    print(f"  {'-'*62}")

    for key, sc in THERMAL_SCENARIOS.items():
        theta = board_theta(area, sc["h"])
        dt = p_board * theta
        tj25 = 25 + dt
        tj40 = 40 + dt
        w = " !! EXCEED" if tj25 > 150 else " ! HOT" if tj25 > 125 else ""
        print(f"  {sc['label']:<28s} {theta:5.1f}°/W  +{dt:4.0f}°C  {tj25:6.0f}°C  {tj40:6.0f}°C{w}")

    # ─── Transient thermal ───
    print(f"\n  Transient thermal (time to Tj=150°C from 25°C ambient):")
    print(f"  Board thermal mass: {c_th:.2f} J/K")
    print(f"  {'Scenario':<28s} {'τ':>6s}  {'t to 150°C':>10s}")
    print(f"  {'-'*50}")

    for key, sc in THERMAL_SCENARIOS.items():
        theta = board_theta(area, sc["h"])
        tau = c_th * theta
        t_max = transient_time_to_tj(p_board, theta, c_th, 150, 25)
        if t_max == float('inf'):
            t_str = "never"
        elif t_max < 1:
            t_str = f"{t_max*1000:.0f} ms"
        else:
            t_str = f"{t_max:.1f} s"
        print(f"  {sc['label']:<28s} {tau:5.1f}s   {t_str:>10s}")

    # ─── MOSFET limits ───
    p_worst_fet = max(
        losses["p_cond_hs"] + losses["p_switch"] + losses["p_dead"]/2 + losses["p_rr"],
        losses["p_cond_low"] + losses["p_body"] + losses["p_dead"]/2,
    )
    print(f"\n  MOSFET: RθJC={p['rth_jc']:.2f}°C/W  Pd_max={p['pd_max']:.0f}W  Tj_max={p['tj_max']:.0f}°C")
    print(f"  Worst single FET: {p_worst_fet:.2f}W → ΔTjc={p_worst_fet*p['rth_jc']:.1f}°C above pad")
    print("=" * 70)


def sweep(profile_key: str, currents: list, v_bus: float, duty: float,
          f_pwm: float, comp_pwm: bool, dead_time: float, n_active: int):
    p = PROFILES[profile_key]
    area = p["board_area"]
    c_th = board_thermal_mass(area, p["layers"], p["oz_outer"], p["oz_inner"])
    theta_fly = board_theta(area, 100)  # strong prop wash

    print()
    print(f"  {p['name']}  @  {v_bus:.0f}V  {duty*100:.0f}%  {f_pwm/1e3:.0f}kHz  "
          f"comp_pwm={'ON' if comp_pwm else 'OFF'}")
    print(f"  Board: {area:.0f}mm²  θ_propwash={theta_fly:.1f}°/W  C_th={c_th:.2f}J/K")
    print(f"  {'I':>6s}  {'Phase':>7s}  {'Board':>7s}  {'Eff':>5s}  "
          f"{'Tj_fly':>6s}  {'t→150°C':>8s}  {'Rating':>12s}")
    print(f"  {'-'*66}")

    for current in currents:
        losses = calc_phase_losses(current, v_bus, duty, f_pwm, comp_pwm, dead_time, p)
        p_board = losses["p_total"] * n_active
        p_motor = v_bus * current * duty * n_active
        eff = p_motor / (p_motor + p_board) * 100 if p_motor > 0 else 0
        tj_fly = 25 + p_board * theta_fly
        t_max = transient_time_to_tj(p_board, theta_fly, c_th, 150, 25)

        if t_max == float('inf'):
            t_str = "∞"
            if tj_fly < 100:
                rating = "continuous"
            elif tj_fly < 125:
                rating = "continuous*"
            else:
                rating = "marginal"
        elif t_max > 10:
            t_str = f"{t_max:.0f}s"
            rating = "burst OK"
        elif t_max > 3:
            t_str = f"{t_max:.1f}s"
            rating = "burst limit"
        else:
            t_str = f"{t_max:.1f}s"
            rating = "DANGER"

        print(f"  {current:5.0f}A  {losses['p_total']:6.2f}W  {p_board:6.1f}W  "
              f"{eff:4.1f}%  {tj_fly:5.0f}°C  {t_str:>8s}  {rating:>12s}")

    print()
    print("  continuous  = Tj < 100°C steady-state in prop wash")
    print("  continuous* = Tj 100-125°C (hot but survivable)")
    print("  marginal    = Tj 125-150°C (near limit)")
    print("  burst OK    = >10s to Tj_max (typical punch-out)")
    print("  burst limit = 3-10s to Tj_max")
    print()


def compare_boards(v_bus: float, duty: float, f_pwm: float, comp_pwm: bool,
                   dead_time: float, n_active: int):
    """Side-by-side comparison of both ESC variants."""
    currents = [5, 10, 15, 20, 25, 30, 35, 40, 50]

    print()
    print("=" * 78)
    print("  BOARD COMPARISON  —  20×20 vs 30×30")
    print(f"  {v_bus:.0f}V  {duty*100:.0f}% duty  {f_pwm/1e3:.0f}kHz  "
          f"comp_pwm={'ON' if comp_pwm else 'OFF'}  {n_active} phases")
    print("=" * 78)

    for key in ["20x20", "30x30"]:
        p = PROFILES[key]
        area = p["board_area"]
        c_th = board_thermal_mass(area, p["layers"], p["oz_outer"], p["oz_inner"])
        theta_fly = board_theta(area, 100)
        rds_hot = p["rds_on"] * p["rds_tempco"]

        print(f"\n  {p['name']}")
        print(f"  Rds(on)={rds_hot*1e3:.1f}mΩ hot  Rg={p['rg']:.0f}Ω  "
              f"Qrr={p['qrr']*1e9:.0f}nC  RθJC={p['rth_jc']:.2f}°/W")
        print(f"  θ_fly={theta_fly:.1f}°/W  C_th={c_th:.2f}J/K  "
              f"R_cu={p['r_copper']*1e3:.1f}mΩ/phase")
        print(f"  {'I':>6s}  {'Board W':>7s}  {'Eff':>5s}  "
              f"{'Tj_fly':>6s}  {'t→150°C':>8s}")
        print(f"  {'-'*44}")

        for current in currents:
            losses = calc_phase_losses(current, v_bus, duty, f_pwm, comp_pwm, dead_time, p)
            p_board = losses["p_total"] * n_active
            p_motor = v_bus * current * duty * n_active
            eff = p_motor / (p_motor + p_board) * 100 if p_motor > 0 else 0
            tj_fly = 25 + p_board * theta_fly
            t_max = transient_time_to_tj(p_board, theta_fly, c_th, 150, 25)
            t_str = "∞" if t_max == float('inf') else f"{t_max:.1f}s" if t_max < 60 else f"{t_max/60:.0f}m"
            warn = " !!" if tj_fly > 150 else " !" if tj_fly > 125 else ""
            print(f"  {current:5.0f}A  {p_board:6.1f}W  {eff:4.1f}%  "
                  f"{tj_fly:5.0f}°C  {t_str:>8s}{warn}")

    print()


def compare_pcb_options(profile_key: str, i: float, v_bus: float, duty: float,
                        f_pwm: float, comp_pwm: bool, dead_time: float, n_active: int):
    """Show impact of different PCB stackups on thermal performance."""
    p = PROFILES[profile_key]

    print()
    print(f"  PCB stackup comparison for {p['name']} @ {i:.0f}A {v_bus:.0f}V {duty*100:.0f}%")
    print("=" * 78)
    print(f"  {'Option':<38s} {'R_cu':>5s} {'Board W':>7s} {'Tj_fly':>6s} "
          f"{'t→150':>6s} {'Notes'}")
    print(f"  {'-'*76}")

    for opt_key, opt in PCB_OPTIONS.items():
        r_cu = copper_resistance_scaled(p["r_copper"], p["oz_outer"], opt["oz_outer"])
        losses = calc_phase_losses(i, v_bus, duty, f_pwm, comp_pwm, dead_time, p,
                                   r_copper_override=r_cu)
        p_board = losses["p_total"] * n_active
        area = p["board_area"]
        c_th = board_thermal_mass(area, opt["layers"], opt["oz_outer"], opt["oz_inner"])
        theta_fly = board_theta(area, 100)
        tj = 25 + p_board * theta_fly
        t_max = transient_time_to_tj(p_board, theta_fly, c_th, 150, 25)
        t_str = "∞" if t_max == float('inf') else f"{t_max:.1f}s"

        print(f"  {opt['label']:<38s} {r_cu*1e3:4.1f}  {p_board:6.1f}W  "
              f"{tj:5.0f}°C  {t_str:>5s}  {opt['notes']}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="4in1 ESC power loss calculator (AM32 6-step trapezoidal)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s -p 20x20 -i 30 -v 16.8 -d 80
  %(prog)s -p 30x30 -i 40 -v 25.2 -d 50 --comp-pwm
  %(prog)s -p 20x20 --sweep 5,10,15,20,25,30,35,40
  %(prog)s --compare -v 16.8 -d 80
  %(prog)s --pcb-options -p 30x30 -i 30 -v 16.8 -d 80
""")
    parser.add_argument("-p", "--profile", choices=["20x20", "30x30"], default="20x20",
                        help="ESC variant (default: 20x20)")
    parser.add_argument("-i", "--current", type=float, default=30.0)
    parser.add_argument("-v", "--voltage", type=float, default=16.8)
    parser.add_argument("-d", "--duty", type=float, default=80.0)
    parser.add_argument("-f", "--pwm-freq", type=float, default=24000)
    parser.add_argument("--dead-time", type=float, default=200e-9)
    parser.add_argument("--comp-pwm", action="store_true")
    parser.add_argument("-n", "--num-active", type=int, default=4)
    parser.add_argument("--sweep", type=str, default=None)
    parser.add_argument("--compare", action="store_true",
                        help="compare 20x20 vs 30x30 side by side")
    parser.add_argument("--pcb-options", action="store_true",
                        help="compare PCB stackup options")

    args = parser.parse_args()
    duty = args.duty / 100.0

    if args.compare:
        compare_boards(args.voltage, duty, args.pwm_freq, args.comp_pwm,
                       args.dead_time, args.num_active)
    elif args.pcb_options:
        compare_pcb_options(args.profile, args.current, args.voltage, duty,
                            args.pwm_freq, args.comp_pwm, args.dead_time, args.num_active)
    elif args.sweep:
        currents = [float(x) for x in args.sweep.split(",")]
        sweep(args.profile, currents, args.voltage, duty, args.pwm_freq,
              args.comp_pwm, args.dead_time, args.num_active)
    else:
        print_full_report(args.profile, args.current, args.voltage, duty,
                          args.pwm_freq, args.comp_pwm, args.dead_time, args.num_active)


if __name__ == "__main__":
    main()
