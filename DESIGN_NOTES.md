# Design Notes — 4in1 ESC

Engineering rationale for the key design choices on this board. Written for anyone reviewing the design, porting it, or adapting it for a different cell count / current class.

## Dead time

Dead time is set in firmware (AM32) and is also bounded below by the gate driver's internal minimum dead time. The NSG2065Q and FD6288Q-family clones all enforce an internal minimum of ~200 ns, so firmware values below that floor have no effect on the output. The TI DRV8300 is the exception — it exposes dead time on the DT pin, minimum ~80 ns with the pin floating.

Two practical tuning methods:

1. **Empirical.** Reduce dead time in steps while monitoring motor current and FET/driver temperature on a bench setup. When either starts climbing, back off a few steps as margin. Shoot-through manifests as a sudden input current spike and usually a dead FET, so current-limit the supply.
2. **Scope-based.** Probe both gate-source voltages simultaneously (differential probe on the high side, or two passive probes with math). Adjust until there is no Vgs overlap at the switch-node transition, plus a small visible dead band.

Shipped default is conservative — tune only if there is a reason (measured efficiency headroom, audible commutation noise).

## MOSFET Vds margin

The SP40N03GNJ is rated 40 V Vds. On 6S (25.2 V fully charged) this leaves ~15 V for switching-edge overshoot and hot-plug ring-up, which is sufficient with the loop geometry used here. 7S is tight but has shipped on comparable commercial boards. 8S on 40V is commercially shipped (T-Motor F55A Pro III) but is aggressive and requires either a TVS clamp or tightly controlled switching edges.

**Important:** datasheet V(BR)DSS is a *minimum* guaranteed breakdown, not typical. Manufacturer app notes (Infineon, Toshiba, onsemi, ST) all recommend that designers add their own 20%+ margin on top of the datasheet number for inverter service. There is no hidden headroom to exploit — die breakdown is typically only ~10-30% above the spec minimum before destructive avalanche.

For a cell-count-up variant, the first-order move is a higher-Vds MOSFET rather than just trusting the existing part.

## Bulk capacitance and hot-plug ring-up

Battery leads have ~100-500 nH of parasitic inductance depending on length. When the battery is connected, that inductance resonates with the ESC bulk capacitance and can ring up to ~1.8-2× battery voltage before damping takes over. This is the single most common ESC failure mode in the field — the first thing the board sees is a voltage spike, not a clean DC rail.

Mitigations used here:

- Multiple low-ESR ceramics placed directly at each half-bridge.
- Recommended external electrolytic of 470 µF low-ESR on the battery pads (user-added, typical for 4-in-1 ESCs in this class).
- Rating: external electrolytic voltage should be at least 2× battery max (63 V for 8S) for ripple-current life.
- ESR and ESL of the bulk cap matter more than raw capacitance. A single high-ESR electrolytic will not catch the LC ring.

Lead quality also matters: copper-clad aluminum or copper-coated steel wire has 50-500% higher resistance than solid copper, heats up under load, and that heating raises resistance further. Only use silicone-insulated tinned copper for battery leads at 60+ A.

A TVS is a possible addition but has a trade-off: a TVS sized close to Vbat(max) leaks under temperature and occasional operation, while one sized well above clamps at a voltage that may already exceed the FET Vds rating. Example: an SMBJ33CA clamps at ~53 V, already above the 40 V FET rating.

## Commutation loop and switching spike

The relevant inductance for the switching spike is the commutation loop:

```
bulk cap → high-side FET → low-side FET → source return → cap
```

V_spike = L_loop × di/dt. Keeping this loop small is the single most important layout constraint on the board. On this design:

- Ceramics are placed between each half-bridge and its adjacent return path, not only at the battery input.
- Half-bridge loop routing uses the inner layers where possible to reduce loop area.
- Gate resistors (4.7 Ω shipped) are sized to keep Vds overshoot within budget at typical Fsw. Slower edges are preferred over faster edges on racing ESCs because conduction loss dominates at 24-48 kHz — switching loss is a small fraction of the total.

Be aware that RLC resonances (parallel or series) in the loop can be harder to spot than clean overshoot. Probe with a short ground spring, not a long clip lead, or you will be measuring the probe ringing.

## Switching frequency

AM32 defaults to 24/48 kHz auto (24 kHz at low RPM, 48 kHz at high RPM). BLHeli_S is hardcoded at 24 kHz. At these frequencies:

- Conduction loss (I² × Rds(on) × duty) dominates.
- Switching loss (½ × V × I × (tr+tf) × Fsw) is small enough that adding gate resistance to soften edges is a good trade for EMI and Vds overshoot.
- Larger gate resistors reduce dV/dt, reduce radiated EMI, and reduce stress on the MOSFET avalanche budget.

This is the opposite trade-off to a high-Fsw SMPS where switching loss dominates and fast edges are mandatory.

## MCU/logic power supply

The 3V3 rail is generated by an LMR51420YDDCR buck with a 470 nH inductor, followed by a TLV76733DRVR LDO for the 3V3 analog/MCU rail.

The 470 nH inductor is well below TI's datasheet recommendation (2.2-4.7 µH for a 2A output). It works here because the actual load is 50-200 mA (MCU, gate driver logic side, sensor amp) — the converter operates with very high ripple current and spends most of the cycle in near-DCM, but peak inductor current stays well below the 3.7 A limit. This is an area-optimization choice; the IC selection was driven by inventory standardization rather than strict datasheet compliance.

The cascaded LDO cleans the buck ripple for the MCU, ADC reference, and current-sense amplifier, which are the parts of the system that actually need a clean rail. The gate driver logic side tolerates a few tens of mV of ripple on its VCC. A direct LDO from battery voltage would dissipate 2-3 W on 6S/8S and is not thermally viable in a SOT-23/WSON package — that is why the buck stage exists at all even though the load is small.

## Bring-up checklist

For a new board, new drone, or a replacement ESC on an existing drone:

1. **Power from current-limited bench supply** at battery voltage (no LiPo), props off. Limit to ~2 A. Idle current should be <100 mA per channel.
2. **Motor direction** per channel via BLHeliSuite / AM32 Configurator. Set before anything else.
3. **Spin each motor individually** in the configurator at low-to-mid throttle. Listen for desync stutter. If it stutters, adjust timing advance or demag compensation.
4. **DShot beacon test** — confirms each output maps to the expected motor and the signal line is clean.
5. **Telemetry over DShot** — verify RPM, current, voltage come through in the Betaflight OSD before arming.
6. **BEC under realistic load** — FC + camera + VTX actually powered. Check rail voltage and ripple with a scope. Load-step if possible.
7. **Thermal check on first spin-up** — thermal camera on the FETs and gate driver during a mid-throttle hold, looking for channel-to-channel uniformity.
8. **Current-sense calibration** against a known load.
9. **Full-throttle punch** on a tether or in a vice with props, then pull Blackbox / BLHeli logs and look at temps, peak current, and desync events.

First plug of a fresh design should always be on a current-limited bench supply, never a LiPo. If something is wrong, the bench supply catches it.
