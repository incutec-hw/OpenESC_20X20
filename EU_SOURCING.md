# OpenDrone ESC — EU Component Sourcing Research

Research doc for the V2 "EU-sourced premium" SKU of the OpenDrone 4-in-1 ESC.

**V1** ships on current AT32F421 + NSG2065Q + SP40N03GNJ BOM via LCSC/JLCPCB (no changes).

**V2** is a separate premium SKU targeting fully EU supply chain: ST fab (France/Italy) MCU, EU-franchised gate driver + MOSFETs, EU PCB fab + assembly (Eurocircuits / Aisler / PCBWay EU turnkey). Positioning is "top performance + western supply chain," not lowest cost.

---

## 1. MCU — Decided

**STM32C531EBU6** (ST, UFQFPN-24 4×4 mm, 128 KB flash, 64 KB RAM, Cortex-M33 @ 144 MHz + FPU + DSP)

- Drop-in-size replacement for current AT32F421G8U7 (both 4×4 QFN), despite 24 vs 28 pin count
- $0.64 @ 10k, made in ST Crolles (FR) / Catania (IT)
- Status: **Preview** — listed at Avnet Silica + EBV, **stock 0 everywhere** as of April 2026, 13–53 week lead time. Not production-ready yet.
- AM32 port: not yet supported, Alka is planning port. AM32 already supports STM32G071 (M0+) which shares most peripheral IP with C5. Port estimate ~2–3 weeks based on AM32 codebase audit.

Backup / bridge path: **STM32G071G8U6** (28-pin UFQFPN 4×4, already AM32-supported, EU-stocked today). Alka confirmed "28-pin G071 is more than sufficient" — this is a zero-risk fallback if C5 production slips.

### V2 plan

1. Wait for STM32C531EB production stock to land (likely Q3 2026)
2. Wait for AM32 STM32C5 port to merge (Alka, likely parallel with ST production)
3. Spin V2 PCB on C5 once both available
4. Provide Alka bring-up boards during port development

---

## 2. 3-Phase Gate Driver

### Constraint recap

- Package ≤ 4×4 mm QFN (hard — PCB footprint locked)
- 3-phase half-bridge driver with bootstrap high-side
- AM32 compatible: 6 logic-level PWM inputs (3× HI + 3× LI), no SPI
- 7–30 V supply, 3.3 V logic inputs
- Source/sink ≥ 500 mA peak

### Candidates screened

| MPN | Mfr | Package | 3-phase | Logic inputs | SPI | Fits |
|---|---|---|---|---|---|---|
| **DRV8300DRGER** | TI | QFN-24 4×4 | Yes | 6× HI/LI | No | **YES** |
| **STDRIVE101** | ST | VFQFPN-24 4×4 | Yes | 6× HI/LI | No | **YES** (pinout differs from NSG2065Q) |
| 6ED2742S01Q | Infineon | QFN-32 5×5 | Yes | PWM+EN | No | Package too big |
| 6EDL7141 | Infineon | VQFN-48 7×7 | Yes | Yes | Required | Too big + SPI |
| RAA227063 | Renesas | QFN-48 7×7 | Yes | Yes | Required | Too big + SPI |
| MP6540H | MPS | QFN-26 5×5 | Yes (integrated FETs) | Yes | No | Too big + integrated FETs |
| MCP8024 | Microchip | QFN-40 5×5 | Yes | Yes | No | Too big |
| STDRIVE601 | ST | SO-28 | Yes | Yes | No | Wrong package |
| NCP51820 | onsemi | QFN-15 4×4 | Half-bridge | Yes | No | Needs 3 chips |
| DGD0506 | Diodes | W-DFN-10 | Half-bridge | Yes | No | Needs 3 chips |
| L6491D | ST | SO-16 | Half-bridge | Yes | No | Needs 3 chips |
| LMG1210 | TI | WQFN-19 3×4 | Half-bridge | Yes | No | Needs 3 chips |

Only two parts fit all hard constraints. Infineon 3-phase EiceDRIVER family is all 5×5 or 7×7 with mandatory SPI — does not fit 4×4 constraint. No way around this short of moving to 3× half-bridge chips, which the board area doesn't allow.

### DRV8300DRGER — TOP PICK

- **Package**: 24-VQFN (RGE), 4.0×4.0 mm, 0.5 mm pitch. **Pin-compatible with NSG2065Q** per existing ALTERNATIVES.md (pin 5 = MODE, pin 21 = DT, both safe floating; NC pins 5/7/8/21 have no copper on current PCB).
- **Inputs**: 6× HI/LI logic-level 3.3 V / 5 V, non-inverting. Drop-in firmware path — identical to FD6288Q family, zero AM32 porting work.
- **Drive**: 750 mA source / 1.5 A sink peak. VCC 8–60 V. Use "D" variant (integrated bootstrap diodes); "N" variant requires external diodes.
- **Protections**: UVLO on VCC/VDRV/VCP, thermal shutdown. No OCP — simpler, AM32-friendly (OC handled by MCU sense-amp path).
- **EU availability (verified)**: 
  - DigiKey 35,899 stock; $0.83/1pc, $0.468/100, **$0.4025/1k**, ~$0.36/15k. 12-week mfr lead.
  - Mouser EU / Farnell EU / Avnet / Rutronik — all TI franchises.
- **Status**: Active, in-production, global.
- **AM32 porting**: Zero. Behaves identically to current NSG2065Q.

**One-line**: $0.40/1k, 35k+ stock, zero rework, zero porting. Nothing to argue with.

### STDRIVE101 — Premium alternative

- **Package**: VFQFPN-24 4×4 mm. Same outline as NSG2065Q but **pinout is NOT identical** — pinout rework required.
- **Inputs**: Mode-configurable. Mode 1 = 6 inputs INHx/INLx (identical to NSG2065Q). Mode 2 = 3 PWM + 3 EN with programmable deadtime.
- **Drive**: 600 mA source/sink, 5.5–75 V, 40 ns propagation delay (faster than FD6288Q family → better EMI at high duty).
- **Protections**: **Per-FET VDS monitoring with true OC sensing** (stronger than DRV8300), thermal shutdown, standby, integrated bootstrap diodes, **integrated 12 V LDO** (saves BOM line for bootstrap rail).
- **EU availability**: DigiKey 1,361 stock, $1.96/1, $1.17/100, **$1.03/1k**, $0.97/5k. ST universally franchised EU.
- **Status**: Active. Automotive-grade STDRIVE101A variant exists.
- **AM32 porting**: Zero firmware change (logic-level inputs), but **one PCB respin** for pinout.

**One-line**: 2.5× the cost of DRV8300 but VDS-sense OCP + integrated 12 V LDO. Use for V2 if respinning PCB anyway.

### Gate driver verdict for V2

Primary: **DRV8300DRGER** — zero-risk drop-in. US-HQ company but fully EU-distributed.

Optional upgrade: **STDRIVE101** if V2 respin is happening — VDS-sense OCP is a genuine reliability improvement and the integrated LDO simplifies power tree. Also keeps the MCU + gate driver both ST-branded (marketing story for "EU premium" SKU).

---

## 3. Low-Side MOSFETs — 30V, 3.3×3.3 or 3×3 Package

### Constraints

- Package: 3.3×3.3 source-down preferred (new footprint, better thermals), or 3×3 drain-down acceptable
- VDS ≥ 30V (6S racing margin)
- RDS(on) ≤ 3 mΩ @ 10V, ≤ 5 mΩ @ 4.5V (logic level **mandatory** — 3.3 V MCU, 4.5 V gate drive after bootstrap margin)
- ID ≥ 60A

### Candidates (24 pcs per 4-in-1 ESC)

| # | MPN | Mfr | Pkg | VDS | Rds@10V | Rds@4.5V | Qg | S-Down | EU Stock | $/1k | $/10k | 24× |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **PSMN1R6-30MLHX** | Nexperia | LFPAK33 3.3×3.3 | 30V | 1.9 mΩ | ~3.0 mΩ | 41 nC | Drain | 902 DK verified | **$0.50** | **$0.41** | **$9.84** |
| 2 | PSMN1R8-30MLH | Nexperia | LFPAK33 3.3×3.3 | 30V | 2.1 mΩ | ~3.3 mΩ | ~38 nC | Drain | ~2–5k Mouser EU | ~$0.45 | ~$0.38 | ~$9.12 |
| 3 | PSMN2R9-30MLC | Nexperia | LFPAK33 3.3×3.3 | 30V | 2.95 mΩ | 4.5 mΩ | 27 nC | Drain | High | ~$0.35 | ~$0.28 | ~$6.72 |
| 4 | SiSS04DN-T1-GE3 | Vishay | PowerPAK 1212-8S | 30V | 1.2 mΩ | 1.85 mΩ | 28.7 nC | Drain | Farnell DE | ~$0.70 | ~$0.60 | ~$14.40 |
| 5 | SiSD5300DN | Vishay | PowerPAK 1212-F | 30V | 0.71 mΩ | — | low | Source-flip | New/limited | ~$1.00+ | — | >$24 |
| 6 | IQE020N03LM5CG | Infineon | PQFN 3.3×3.3 SD | 30V | 2.0 mΩ | ~3.2 mΩ | ~30 nC | Source | Check Avnet/Rutronik | ~$0.55 | ~$0.50 | ~$12.00 |
| 7 | IQE012N03LM5CG | Infineon | PQFN 3.3×3.3 SD | 30V | 1.15 mΩ | ~1.9 mΩ | ~48 nC | Source | Check Avnet/Rutronik | ~$0.70 | ~$0.65 | ~$15.60 |
| 8 | IQE008N03LM5SC | Infineon | PQFN 3.3×3.3 SD | 30V | 0.85 mΩ | 1.4 mΩ | 64 nC | Source | **OOS at Infineon direct** | ~$0.83 | ~$0.78 | ~$18.72 |
| 9 | NTTFSSCH0D7N02X | onsemi | WDFN9 3.3×3.3 | **25V** | **0.58 mΩ** | — | 55 nC | Source | 1,619 DK verified | $0.96 | $0.79 @5k | $18.96 |
| — | NCEP3065QU (ref only) | NCE | DFN 3.3×3.3 | 30V | 4.5 mΩ typ | 7 mΩ | — | Drain | **LCSC only** | — | — | — |

Row 1, 4, 9 verified from distributor product pages. Rows 2, 3, 6, 7, 8 are estimated from distributor ladder patterns — confirm via Octopart before PO.

### Logic-level gotcha

AM32 on 3.3 V MCU drives ~4.5 V gate after bootstrap. **Only true logic-level parts (Nexperia "LH" suffix, Infineon "LM") hit ≤5 mΩ at 4.5 V.** Standard-level parts (PSMN-xx-MLC non-H) can be 2–3× the 10 V Rds at 4.5 V — avoid.

### Low-side MOSFET picks by tier

| Tier | Pick | 24× | Rationale |
|---|---|---|---|
| **Budget floor (drain-down)** | **PSMN1R6-30MLHX** | **$9.84** | Only part that hits $10 with logic-level + verified EU stock. For a price-sensitive V2 SKU. |
| **Sweet spot (drain-down)** | **Vishay SiSS04DN** | **$14.40** | 1.2 mΩ @ 10V + 28.7 nC Qg = meaningfully lower switching loss. Big EMC win on 6S. |
| **Source-down entry** | **IQE020N03LM5CG** | **$12.00** | Cheapest Infineon source-down + new footprint value prop |
| **Source-down sweet spot** | **IQE012N03LM5CG** | **$15.60** | 1.15 mΩ source-down = real premium story |
| **Source-down king** | IQE008N03LM5SC | $18.72 | Best-in-class 30V; **stock allocation problems — don't lock in** |
| **Absolute king** | NTTFSSCH0D7N02X | $18.96 | 0.58 mΩ onsemi T10 source-down, 25V (ok for 6S racing), 1,619 stock DK |

### Budget reality

Target was $10 / 24 = $0.42/unit (LCSC pricing). EU channel markup adds 50–100% on discretes. Realistic EU floors:
- **Drain-down logic-level**: $10–14 / 24 for 1.2–2 mΩ range
- **Source-down**: $12–19 / 24 for 2–0.6 mΩ range

### V2 recommendation — low-side

For the "EU premium" V2 positioning, spend the extra and go source-down. **IQE012N03LM5CG** ($15.60 / 24) gives the full "Infineon OptiMOS source-down" marketing story plus genuinely better thermal performance. The new footprint is going in anyway per SOURCE-DOWN-OVERVIEW.md.

If budget pressure returns: **PSMN1R6-30MLHX** ($9.84 / 24) — Nexperia is Dutch, still fully EU story, drain-down uses existing footprint.

---

## 4. High-Side / Single-ESC MOSFETs — 40V, 5×6 Package

For the future single-ESC variant in the OpenDrone product line. 6S with headroom.

### Constraints

- Package: PQFN 5×6 source-down or standard LFPAK56 / SuperSO8 / SO-8FL
- VDS ≥ 40V
- RDS(on) ≤ 1 mΩ @ 10V target (1.5 mΩ @ 4.5V)
- ID ≥ 150A

### Candidates

| # | MPN | Mfr | Pkg | VDS | Rds@10V | Rds@4.5V | Qg | ID | EU Stock | $/1k | $/10k | 24× |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **NTMFS5C430NT1G** | onsemi | SO-8FL 5×6 | 40V | 1.7 mΩ | ~2.8 mΩ | 47 nC | 185A | **2,355 DK verified** | **$0.479** | ~$0.42 | **~$10.08** |
| 2 | **PSMN1R4-40YLDX** | Nexperia | LFPAK56 5×6 | 40V | **1.4 mΩ** | ~2.4 mΩ | 96 nC | 100A | **2,342 DK verified** | **$0.679** | **$0.56** | **$13.44** |
| 3 | PSMN1R8-40YLC,115 | Nexperia | LFPAK56 5×6 | 40V | 1.8 mΩ | ~3.1 mΩ | ~80 nC | 100A | DK/Mouser EU | ~$0.60 | ~$0.50 | ~$12.00 |
| 4 | PSMN2R0-40YLB | Nexperia | LFPAK56 5×6 | 40V | 2.1 mΩ | — | ~55 nC | 180A | EU stocked | ~$0.50 | ~$0.40 | ~$9.60 |
| 5 | TPHR8504PL | Toshiba | SOP-8A 5×6 | 40V | 0.85 mΩ | 1.5 mΩ | ~80 nC | 150A | Farnell/TME EU | ~$1.20 | ~$1.00 | ~$24.00 |
| 6 | NTTFSSCH1D3N04XL | onsemi | 5×6 SD T10 | 40V | 1.3 mΩ | — | 3.4 nC Qgd | 276A | **86 pcs Mouser (LOW)** | ~$1.30 | — | ~$31.20 |
| 7 | IQD005N04NM6CG | Infineon | SuperSO8 5×6 | 40V | 0.47 mΩ | 0.7 mΩ | 93 nC | 220A | Check Rutronik/Avnet | ~$1.50 | ~$1.43 | ~$34.32 |
| 8 | IQDH45N04LM6CG | Infineon | SuperSO8-SD 5×6 | 40V | **0.45 mΩ** | 0.7 mΩ | 96 nC | 220A | Check Rutronik/Avnet | ~$1.52 | ~$1.45 | ~$34.80 |

Rows 1, 2 verified. Others estimated/interpolated.

### 5×6 MOSFET picks by tier

| Tier | Pick | 24× | Rationale |
|---|---|---|---|
| **Budget floor** | PSMN2R0-40YLB | ~$9.60 | Hits $10 but standard level — verify 4.5V Rds before committing |
| **Budget+ verified** | **NTMFS5C430NT1G** | **$10.08** | Just over $10, verified stock, logic level. Good $/mΩ |
| **Sweet spot** | **PSMN1R4-40YLDX** | **$13.44** | NextPower-S3 SchottkyPlus reduces spike → EMC win at 6S. Nexperia EU HQ |
| **Premium non-SD** | TPHR8504PL | ~$24 | Best-in-class 0.85 mΩ without going source-down |
| **Source-down king** | IQDH45N04LM6CG | ~$35 | 0.45 mΩ, full Infineon story, 3.5× budget |

### V2 recommendation — 5×6 high-side

For single-ESC premium variant: **PSMN1R4-40YLDX** ($13.44 / 24). Nexperia is EU-HQ (Dutch), NextPower-S3 SchottkyPlus reduces body-diode recovery spike which helps EMC compliance at 6S. 1.4 mΩ @ 10V is excellent.

If source-down marketing matters more than cost: **IQDH45N04LM6CG** at ~$35/24. 0.45 mΩ is 3× better than the Nexperia — genuinely high-end, but 2.6× the price.

---

## 5. Power Supply (Buck + LDO)

Both current parts are TI — already EU-distributed via Mouser/Farnell/DigiKey. Keep unless an ST equivalent provides a stronger "EU-branded" story.

### Buck converter (current: LMR51420XDDCR)

Keep **TI LMR51420XDDCR** (SOT-23-6). 5,282 stock on LCSC, also heavily stocked on DigiKey/Mouser EU. ST alternative: **LDL212** or newer ST LDO — worth quick check if full-ST narrative matters.

### 3.3V LDO (current: TLV76733DRVR)

Keep **TI TLV76733DRVR** (WSON-6) or consider ST **LD39015** / **LDL112** for full ST story. Performance equivalent.

---

## 6. Current Sense Amplifier

Current: **TI INA186A3IDCKR** (SC-70-6). TI is EU-distributed. Alternatives if pursuing full-ST:
- **ST TSC1031** (similar SC-70 package, current-shunt amp)
- Keep INA186 — it's already EU-available and performance is known-good.

---

## 7. Passives — Already EU-sourceable

All currently chosen passives are from JP/EU manufacturers with deep EU distribution:

- **Ferrite beads**: Murata BLM03PX121SN1D — keep
- **Inductors**: Use Würth (DE), TDK (JP/DE), Coilcraft (US/EU distributed)
- **Capacitors**: Würth, TDK, Murata, KEMET (FR-based)
- **Resistors**: Vishay, Yageo, Panasonic, Bourns

No changes needed. All available at Mouser EU / Farnell / DigiKey EU.

---

## 8. Connectors

Current signal connector: HC-1.0-8PWT (JLCPCB part). EU alternatives:
- **Molex Pico-EZmate** series
- **JST GH** (JST has EU distribution)
- **Würth WR-WTB** (DE, full EU)

---

## 9. PCB Fab + Assembly

### EU fabs with assembly

- **Eurocircuits (BE)** — full turnkey EU assembly, strong for 2–6 layer prototypes and small runs
- **Aisler (NL)** — lower MOQ, fast turn, good for bring-up boards
- **Multi-CB (DE)** — mid-volume turnkey
- **PCBWay EU** — turnkey EU warehouse option, wider parts library than others
- **JLCPCB** — keep as V1 option; explicitly non-EU for V2

### Assembler research action items

- [ ] Get quote from Eurocircuits for 100 pcs 4-layer 4-in-1 with full BOM
- [ ] Get quote from Aisler for 10 pcs prototype (same BOM)
- [ ] Get quote from PCBWay EU for 100 pcs turnkey
- [ ] Confirm which assemblers stock Infineon source-down OptiMOS + DRV8300 or require free-issue

---

## 10. Distributor Strategy

| Distributor | Strongest franchise for this BOM | EU warehouse |
|---|---|---|
| **Mouser EU** | TI (DRV8300), Nexperia | DE (Munich) |
| **Farnell / element14** | ST (STM32C5, STDRIVE101), Vishay, Toshiba | UK + DE |
| **Digi-Key EU** | Broad — all brands | DE (Munich) |
| **Avnet Silica** | Infineon OptiMOS, ST STM32C5 volume | EU-wide |
| **EBV Elektronik** | NXP/Nexperia allocation | EU-wide |
| **Rutronik** | Infineon volume orders | DE |

For production volume (≥5k units), **Avnet Silica + Rutronik** will negotiate Infineon source-down volume pricing below the budgetary €/1k shown on Infineon's site.

---

## 11. V2 Recommended BOM (Premium EU SKU)

| Block | V1 (current) | V2 premium | 24× cost delta |
|---|---|---|---|
| MCU | AT32F421G8U7 | **STM32C531EBU6** | ~$0 (parity) |
| Gate driver | NSG2065Q | **TI DRV8300DRGER** | ~$0 (parity) |
| Low-side MOSFET ×24 | SP40N03GNJ | **Infineon IQE012N03LM5CG** | +$13 |
| Buck | LMR51420XDDCR | Same (TI EU) | $0 |
| LDO | TLV76733DRVR | Same (TI EU) | $0 |
| Current sense | INA186A3IDCKR | Same (TI EU) | $0 |
| Ferrite | BLM03PX121SN1D | Same (Murata EU) | $0 |

**Key BOM delta vs V1: ~+$13 per 4-in-1 in active silicon.** Passives unchanged. PCB fab + assembly move from JLCPCB to EU assembler — separate cost delta (typically +€5–15 per board depending on volume and assembler).

### V2 marketing story

- "STM32C5 Cortex-M33 @ 144 MHz — 3× the compute of typical ESCs"
- "Infineon OptiMOS 5 Source-Down MOSFETs — premium automotive-grade silicon"
- "TI DRV8300 gate driver with integrated bootstrap"
- "Fully EU supply chain — MCU fabbed in France, MOSFETs in Germany/Austria, assembled in [EU assembler]"
- "Open source hardware (CERN-OHL-S) + open source firmware (AM32 MIT/GPL)"

---

## 12. Open Action Items

- [ ] Monitor STM32C531EBU6 production status at Avnet Silica / EBV (currently Preview, stock 0). Check every 4–6 weeks.
- [ ] Track AM32 STM32C5 port progress (Alka). Offer bring-up boards when port is ready.
- [ ] Get production EU assembly quotes (Eurocircuits, Aisler, Multi-CB, PCBWay EU) for V2 BOM at 100 / 500 / 1000 qty.
- [ ] Negotiate Infineon OptiMOS volume pricing through Avnet Silica or Rutronik once V2 goes to production.
- [ ] Decide: Vishay SiSS04DN ($14.40/24, drain-down, keeps existing footprint) vs Infineon IQE012N03LM5CG ($15.60/24, source-down, new footprint). The $1.20 premium for source-down is marginal; the new footprint is the real cost.
- [ ] Decide: DRV8300 (zero rework, TI) vs STDRIVE101 (PCB respin, ST, stronger feature set + EU brand). Respin is happening anyway → lean STDRIVE101.
- [ ] Request STM32C5 samples via Avnet Silica FAE for Alka AM32 port development.
- [ ] Spec a minimal STM32C531 bring-up board (MCU + SWD + UART + LED + 3.3V LDO + USB) for Alka.

---

## 13. Flagged Risks

1. **STM32C531EB is Preview status with 13–53 week lead** — V2 launch timeline depends on ST production ramp. Fallback: STM32G071G8U6 (AM32-supported today, EU-stocked) for an interim "EU supply chain" V1.5.
2. **AM32 STM32C5 port doesn't exist yet** — depends on Alka. Zero work done in AM32 codebase per April 2026 audit.
3. **Infineon IQE008N03LM5 currently OOS at Infineon direct** — don't lock best-Rds source-down into V2 BOM. Use IQE012N03LM5CG or IQE020N03LM5CG which are better-stocked.
4. **Source-down footprint is new** — need 3D model, footprint verification, paste mask tuning. Plan for ≥1 prototype iteration before production.
5. **No Chinese source-down parts exist on any EU franchise** — source-down is Infineon/onsemi/Vishay only, permanent premium tier.
6. **JLCPCB cannot do asymmetric copper** (2oz front only) per existing notes — if EU assembler has same limitation, confirm stackup at quote time.

---

## 14. References

### Primary sources

- [TI DRV8300 product page](https://www.ti.com/product/DRV8300)
- [DRV8300DRGER at DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/DRV8300DRGER/13918763)
- [ST STDRIVE101 datasheet](https://www.st.com/resource/en/datasheet/stdrive101.pdf)
- [STDRIVE101 at DigiKey](https://www.digikey.com/en/products/detail/stmicroelectronics/STDRIVE101/11590991)
- [Nexperia PSMN1R6-30MLH](https://www.nexperia.com/product/PSMN1R6-30MLH)
- [PSMN1R6-30MLHX at DigiKey](https://www.digikey.com/en/products/detail/nexperia-usa-inc/PSMN1R6-30MLHX/8628194)
- [Nexperia PSMN1R4-40YLD](https://www.nexperia.com/product/PSMN1R4-40YLD)
- [PSMN1R4-40YLDX at DigiKey](https://www.digikey.com/en/products/detail/nexperia-usa-inc/PSMN1R4-40YLDX/4965588)
- [NTMFS5C430NT1G at DigiKey](https://www.digikey.com/en/products/detail/onsemi/NTMFS5C430NT1G/6560595)
- [onsemi NTTFSSCH0D7N02X](https://www.onsemi.com/products/discrete-power-modules/mosfets/low-medium-voltage-mosfets/NTTFSSCH0D7N02X)
- [Infineon IQE008N03LM5](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/iqe008n03lm5)
- [Infineon IQE020N04LM6CG](https://www.infineon.com/part/IQE020N04LM6CG)
- [Infineon IQDH45N04LM6](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/iqdh45n04lm6/)
- [Vishay SiSD5300DN press release](https://www.vishay.com/en/company/press/releases/2024/SiSD5300DN/de/)
- [Toshiba TPHR8504PL](https://toshiba.semicon-storage.com/eu/semiconductor/product/mosfets/12v-300v-mosfets/detail.TPHR8504PL.html)

### Related project docs

- `ALTERNATIVES.md` — NSG2065Q gate driver alternatives & pin compatibility
- `SOURCE-DOWN-OVERVIEW.md` — prior source-down analysis
- `DESIGN_NOTES.md` — general design notes
- `MEMORY.md` — project context (auto-memory)
