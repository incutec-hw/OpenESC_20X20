# Source-Down MOSFET Overview — 4in1 ESC

Sub-2mΩ N-channel MOSFETs in 3x3mm / 3.3x3.3mm packages, 25-40V. For mid-range and high-end ESC builds.

**What is Source-Down?** Die is flipped so the source (where heat generates) faces the PCB thermal pad instead of drain. Benefits: ~30% lower RDS(on), ~20% better RthJC (1.4 vs 1.8 K/W), low-side thermal pad becomes GND (thermal vias without switch-node noise coupling). Requires new footprint — thermal pad net changes from drain to source.

**Who has it:** Infineon (OptiMOS Source-Down), onsemi (PowerTrench T10 Source-Down), Vishay (Source Flip). No Chinese manufacturer has source-down technology — this is a packaging gap that will take 2-3+ years to close.

---

## Infineon — OptiMOS Source-Down (PQFN 3.3x3.3mm)

Industry leader. Widest portfolio. Three generations available (OptiMOS 5/6/7).

### 30V Parts

| Part | RDS(on)@10V | RDS(on)@4.5V | Qg@10V | Qg@4.5V | Id | Variant | Price €/1k |
|------|-------------|--------------|--------|---------|-----|---------|------------|
| **IQE008N03LM5** | **0.85mΩ** | 1.4mΩ | 64nC | 30nC | 253A | Corner-gate BSC | €0.78 |
| **IQE008N03LM5CG** | **0.85mΩ** | 1.4mΩ | 64nC | 30nC | 253A | Center-gate BSC | €0.78 |
| **IQE008N03LM5SC** | **0.85mΩ** | 1.0mΩ | 64nC | 30nC | 252A | Corner-gate DSC | €0.87 |
| **IQE008N03LM5CGSC** | **0.85mΩ** | 1.0mΩ | 64nC | 30nC | 252A | Center-gate DSC | €0.87 |
| IQE012N03LM5CG | 1.15mΩ | 1.55mΩ | 40nC | 18.9nC | 224A | Center-gate BSC | NEW |
| IQE012N03LM5CGSC | 1.15mΩ | 1.45mΩ | 40nC | 18.9nC | 224A | Center-gate DSC | NEW |

### 40V Parts

| Part | RDS(on)@10V | RDS(on)@4.5V | Qg@10V | Qg@4.5V | Id | Variant | Price €/1k |
|------|-------------|--------------|--------|---------|-----|---------|------------|
| **IQE010N04LM7CG** | **1.0mΩ** | 1.3mΩ | 39nC | 18.9nC | 271A | CG BSC, OptiMOS 7 | NEW |
| **IQE010N04LM7CGSC** | **1.0mΩ** | 1.3mΩ | 39nC | 18.9nC | 270A | CG DSC, OptiMOS 7 | NEW |
| IQE013N04LM6 | 1.35mΩ | 1.9mΩ | 41nC | 20nC | 205A | Corner-gate BSC | €0.75 |
| IQE013N04LM6CG | 1.35mΩ | 1.9mΩ | 41nC | 20nC | 205A | Center-gate BSC | €0.75 |
| IQE013N04LM6SC | 1.35mΩ | 1.9mΩ | 41nC | 20nC | 205A | Corner-gate DSC | €0.81 |
| IQE013N04LM6CGSC | 1.35mΩ | 1.9mΩ | 41nC | 20nC | 205A | CG DSC | €1.02 |
| IQE020N04LM6CG | 2.05mΩ | 3.0mΩ | 25nC | 12.1nC | 166A | CG BSC, low Qg | NEW |
| IQE020N04LM6CGSC | 2.05mΩ | 2.9mΩ | 25nC | 12.1nC | 166A | CG DSC, low Qg | NEW |

### Variant Suffixes
- **(none)** = Corner-gate, bottom-side cooling (standard pinout, closest to drain-down drop-in)
- **CG** = Center-gate (gate moved to center edge, optimized for paralleling, NOT pin-compatible with standard)
- **SC** = Dual-side cooling (exposed top copper for heatsink)
- **CGSC** = Center-gate + dual-side cooling
- Add **ATMA1** for tape-and-reel ordering

### Availability
- **LCSC: NONE.** Zero Infineon source-down parts stocked.
- **DigiKey:** IQE013N04LM6ATMA1 and CG variant in stock, same-day ship.
- **Mouser:** IQE013N04LM6 variants in stock.
- **Farnell:** Listed, extended lead times on some.
- **NEW parts (OptiMOS 7, IQE010/012/020):** Likely sample/pre-production. Pricing TBD. Watch for availability Q3-Q4 2026.

### Star Parts
- **High-end 30V:** IQE008N03LM5 — 0.85mΩ, best-in-class from Infineon. €0.78/1k.
- **High-end 40V:** IQE010N04LM7CG — 1.0mΩ, OptiMOS 7, NEW. Pricing TBD.
- **Value 40V:** IQE013N04LM6 — 1.35mΩ, established part, €0.75/1k. Best balance.
- **Low-Qg 40V:** IQE020N04LM6CG — 2.05mΩ but only 25nC Qg. Lower switching loss, good for high-frequency PWM.

---

## onsemi — PowerTrench T10 Source-Down (WDFN9 3.3x3.3mm)

Newest generation (T10). Excellent Qgd (3.4nC) — fast switching. Limited availability (new parts).

| Part | Vds | RDS(on)@10V | Qg@10V | Qgd | Id | Package | Availability |
|------|-----|-------------|--------|-----|-----|---------|-------------|
| **NTTFSSCH0D7N02X** | 25V | **0.58mΩ typ / 0.72mΩ max** | ~21nC | 3.4nC | 310A | WDFN9 3.3x3.3 SD DSC | DigiKey 1.6k, ~$0.84-2.59 |
| **NTTFSSCH1D3N04XL** | 40V | **~1.05mΩ typ / 1.3mΩ max** | 47nC | 3.4nC | 207A | WDFN9 3.3x3.3 SD DSC | Mouser 86 pcs, 27-wk lead DK |

### Notes
- **NTTFSSCH0D7N02X** is the lowest RDS(on) of ANY part in this overview (0.58mΩ!) but only 25V — 6S max.
- **NTTFSSCH1D3N04XL** directly competes with Infineon IQE013N04LM6 at 40V. Better Qgd (3.4 vs ~8nC) = much faster switching. But terrible availability right now.
- **No 30V T10 source-down** from onsemi. Gap in their lineup.
- Older gen FDMC8010/8010DC (30V, 1.28mΩ, drain-down, 67nC Qg) still available but terrible gate charge.
- **LCSC: NONE** for any T10 source-down parts.

### Star Parts
- **Ultra-high-end 25V:** NTTFSSCH0D7N02X — 0.58mΩ, untouchable RDS(on). 6S only.
- **High-end 40V:** NTTFSSCH1D3N04XL — 1.3mΩ, best Qgd in class. Supply-constrained.

---

## Vishay — Source Flip (PowerPAK 1212-F, 3.3x3.3mm)

New technology, limited portfolio. "Source Flip" = their branding for source-down.

| Part | Vds | RDS(on)@10V | Qg | Id | Package | Availability |
|------|-----|-------------|-----|-----|---------|-------------|
| **SiSD5300DN** | 30V | **0.71mΩ** | ~59nC | ~100A | PowerPAK 1212-F 3.3x3.3 | NEW, 26-wk lead, limited |
| **SiSS04DN** | 30V | 1.2mΩ | 28.7nC | 80A | PowerPAK 1212-8S 3.3x3.3 | DigiKey in stock, ~$1-1.50 |

### Notes
- **SiSD5300DN** has the lowest RDS(on) of any 30V part (0.71mΩ!) but massive Qg (59nC) and uses the new 1212-F footprint (different pad layout from standard 1212-8).
- **SiSS04DN** is more practical — 1.2mΩ with only 28.7nC Qg. Good switching + good conduction. Standard 1212-8S footprint.
- **No 40V source-down/source-flip** parts from Vishay in 3.3x3.3mm. Their 40V 1212-8 parts are 7+ mΩ.
- **LCSC: NONE** for any sub-2mΩ Vishay PowerPAK parts.

---

## Nexperia — LFPAK33 (3.3x3.3mm, drain-down only)

No source-down technology. Uses copper clip bonding. NextPowerS3 silicon is competitive.

| Part | Vds | RDS(on)@10V | Qg@10V | Qg@4.5V | Id | Package | Price |
|------|-----|-------------|--------|---------|-----|---------|-------|
| **PSMN1R6-30MLH** | 30V | 1.6mΩ typ / 1.9mΩ max | 41nC | 20nC | 160A | LFPAK33 3.3x3.3 | ~$0.70 |
| PSMN1R8-30MLH | 30V | 2.1mΩ max | — | — | 150A | LFPAK33 3.3x3.3 | — |
| PSMN3R3-40MLH | 40V | 3.3mΩ max | — | 17nC | 118A | LFPAK33 3.3x3.3 | — |

### Notes
- **PSMN1R6-30MLH** is a solid 30V part but drain-down. RDS(on) competitive with source-down.
- 40V parts (3.3mΩ) not competitive with Infineon/onsemi source-down.
- **LCSC: NONE** for MLH-suffix NextPowerS3 parts.
- Available at DigiKey, Mouser, TTI. EU-friendly distribution.

---

## TI — NexFET (drain-down only)

No source-down technology. No 40V parts in 3x3mm. Weak in this space.

| Part | Vds | RDS(on)@10V | Qg | Id | Package | DigiKey Price @1k |
|------|-----|-------------|-----|-----|---------|------------------|
| **CSD17575Q3** | 30V | 1.9mΩ typ / 2.3mΩ max | 23nC | 60A | VSON-CLIP-8 3.3x3.3 | $0.36 |

- Only one relevant part. 30V only.
- LCSC: C529277, ~2k stock, $0.43.
- Not competitive with Infineon/onsemi source-down. Skip.

---

## Chinese Manufacturers (drain-down only, LCSC-sourced)

No source-down technology from any Chinese fab. Best options for cost-sensitive builds.

| Part | Mfg | Vds | RDS(on)@10V | Qg | Pkg (mm) | LCSC | Stock | Price |
|------|-----|-----|-------------|-----|----------|------|-------|-------|
| **NCEP3065QU** | NCE Power | 30V | **1.9mΩ** | 34.8nC | 3.3x3.3 | C502964 | ~3,500 | $0.22 |
| **NCEP4065QU** | NCE Power | 40V | **2.2mΩ** | — | 3.1x3.2 | C502974 | ~6,100 | $0.44 |
| APG035N04Q | ALLPOWER | 40V | 2.8mΩ | — | 3.0x3.0 | C5443653 | 3,600 | $0.48 |
| SP40N03GNJ | Siliup | 40V | 2.9mΩ | ~27nC | 3.0x3.0 | C22466709 | 2,125 | $0.10 |
| AON7524 | AOS | 30V | 3.3mΩ | 50nC | 3.0x3.0 | C431195 | 20,400 | $0.22 |

### Notes
- **NCEP3065QU** is the best Chinese sub-2mΩ part. 30V, 1.9mΩ, $0.22, good stock. Competitive with Infineon BSZ0901NS.
- **NCEP4065QU** is the best 40V option under 2.5mΩ on LCSC.
- NCE Power uses "Super Trench" (split-gate trench) — same approach as western fabs but conventional drain-down packaging.
- No Chinese source-down clones expected before 2028+.

---

## LCSC Stock Warning (as of March 2026)

Previously-listed western sub-2mΩ parts are drying up on LCSC:

| Part | Previous Stock | Current Stock | Status |
|------|---------------|---------------|--------|
| FDMC8010DC (C555489) | 2,965 | **~6** | Essentially gone |
| BSZ0901NS (C534685) | 4,035 | **~293** | Declining fast |
| BSZ018N04LS6 (C534643) | 935 | **OOS** | Gone |

**Implication:** Sub-2mΩ parts on LCSC are becoming JLCPCB-incompatible. For premium builds, you'll need either:
1. LCSC consignment (upload your own parts)
2. PCBWay turnkey (they source by MPN globally)
3. EU assembly house with DigiKey/Mouser/Farnell sourcing

---

## Comparison Matrix — Best of Each Tier

### High-End (source-down, EU production)

| Part | Mfg | Vds | RDS(on) | Qg | Qgd | Price est. | Source |
|------|-----|-----|---------|-----|-----|-----------|--------|
| NTTFSSCH0D7N02X | onsemi | 25V | **0.58mΩ** | 21nC | 3.4nC | ~$0.84 | DigiKey |
| SiSD5300DN | Vishay | 30V | **0.71mΩ** | 59nC | — | NEW | Limited |
| IQE008N03LM5 | Infineon | 30V | **0.85mΩ** | 64nC | — | ~€0.78 | DigiKey/Mouser |
| IQE010N04LM7CG | Infineon | 40V | **1.0mΩ** | 39nC | — | NEW | TBD |
| NTTFSSCH1D3N04XL | onsemi | 40V | **1.3mΩ** | 47nC | 3.4nC | ~$0.91 | Mouser (86 pcs) |
| IQE013N04LM6 | Infineon | 40V | **1.35mΩ** | 41nC | — | ~€0.75 | DigiKey/Mouser |

### Mid-Range (drain-down, mixed sourcing)

| Part | Mfg | Vds | RDS(on) | Qg | Price est. | Source |
|------|-----|-----|---------|-----|-----------|--------|
| SiSS04DN | Vishay | 30V | **1.2mΩ** | 28.7nC | ~$1.00 | DigiKey |
| PSMN1R6-30MLH | Nexperia | 30V | **1.6mΩ** | 41nC | ~$0.70 | DigiKey/Mouser |
| NCEP3065QU | NCE | 30V | **1.9mΩ** | 34.8nC | $0.22 | **LCSC** |
| NCEP4065QU | NCE | 40V | **2.2mΩ** | — | $0.44 | **LCSC** |

### Budget (JLCPCB-ready)

| Part | Mfg | Vds | RDS(on) | Qg | Price | LCSC Stock |
|------|-----|-----|---------|-----|-------|-----------|
| SP40N03GNJ | Siliup | 40V | 2.9mΩ | ~27nC | **$0.10** | 2,125 |
| AON7524 | AOS | 30V | 3.3mΩ | 50nC | $0.22 | **20,400** |
| NCEP4065QU | NCE | 40V | 2.2mΩ | — | $0.44 | **6,100** |

---

## Footprint Notes

All source-down parts use 3.3x3.3mm packages. Key differences:

| Package | Thermal Pad | Gate Position | Pin-compatible with drain-down? |
|---------|-------------|---------------|-------------------------------|
| Infineon corner-gate (PG-TSON-8) | SOURCE | Corner (standard) | Same edge pads, thermal pad net swap |
| Infineon center-gate (PG-TTFN-9) | SOURCE | Center edge | **NO** — different pinout |
| onsemi WDFN9 | SOURCE | Center edge | **NO** — center-gate only |
| Vishay 1212-F (Source Flip) | SOURCE | Center | **NO** — different pad layout |

**Only Infineon corner-gate** variants approximate a drain-down footprint. All others need unique footprints.

For the 4in1 ESC, if targeting source-down:
1. Current footprint is 3.0x3.0mm POWERPAK-1212-8 — needs update to 3.3x3.3mm regardless
2. Choose corner-gate (Infineon) for closest compatibility with standard drain-down layout
3. Thermal pad net must change from drain to source in schematic + layout
4. Consider designing a universal footprint that works for both drain-down and source-down (thermal pad connected to both nets via 0R resistor option)

---

## Recommendations

### For V1 production (JLCPCB, cost-sensitive)
Stay with current plan. Source-down parts are not on LCSC. Best LCSC options:
- **Budget:** SP40N03GNJ ($0.10, 2.9mΩ, 40V)
- **Mid-range:** NCEP4065QU ($0.44, 2.2mΩ, 40V) or NCEP3065QU ($0.22, 1.9mΩ, 30V)

### For V2 / EU production (premium ESC)
Source-down becomes viable via DigiKey/Mouser/Farnell + EU assembler or PCBWay turnkey:
- **Best 40V value:** IQE013N04LM6 (1.35mΩ, ~€0.75/1k, in stock)
- **Best 40V performance:** IQE010N04LM7CG (1.0mΩ, OptiMOS 7, NEW — watch for availability)
- **Best 30V if 6S is OK:** IQE008N03LM5 (0.85mΩ, €0.78/1k) or NTTFSSCH0D7N02X (0.58mΩ, ~$0.84)
- **Best switching (low Qgd):** NTTFSSCH1D3N04XL (1.3mΩ, 3.4nC Qgd) — once stock improves

### Cost Impact (12 MOSFETs per ESC, per-unit)

| Tier | Part | MOSFET cost/ESC | vs baseline |
|------|------|----------------|-------------|
| Budget | SP40N03GNJ | $1.20 | baseline |
| Mid-range LCSC | NCEP3065QU | $2.64 | +$1.44 |
| Mid-range LCSC | NCEP4065QU | $5.28 | +$4.08 |
| High-end SD | IQE013N04LM6 | ~$9-12 | +$8-11 |
| Ultra-high-end | IQE008N03LM5 | ~$9-12 | +$8-11 |

---

*Last updated: 2026-03-30. Stock and pricing are approximate — verify before ordering. Source-down availability on LCSC: zero across all manufacturers.*
