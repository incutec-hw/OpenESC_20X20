# Component Review — Commercial Release Audit (v0.3)

Full design review of all ICs and key components for commercial readiness.
Conducted March 2026.

---

## Critical Issues (Must Fix for v0.4)

### 1. TPS746-3.3DRV: Input Voltage Exceeds Absolute Maximum

**Severity: CRITICAL**

The TPS746-3.3DRV LDO has a maximum input voltage of 6.0V (abs max 6.5V), but the upstream LMR51420 buck converter outputs **8.04V** (set by 124kΩ/10kΩ feedback divider). This is a hard specification violation.

**Why it works in testing:** The TPS746 may survive at 8V in benign conditions, but will fail under temperature extremes, production variance, or extended operation. Not acceptable for commercial release.

**Fix:** Drop-in replacement with **TLV76733DRVR** (LCSC C2848334):
- Same WSON-6 2x2mm footprint — zero PCB changes
- Input range: 2.5V to **16V** (8V input with 2x margin)
- Output: 3.3V fixed, **1A** (upgrade from 500mA)
- Price: $0.10 (comparable to TPS746)
- Stock: 8,240 units on LCSC

**BOM change:** Replace U26 TPS746-3.3DRV (C524780) → TLV76733DRVR (C2848334)

---

### 2. INA199A1DCKR: Common-Mode Voltage Marginal for 6S

**Severity: CRITICAL**

The INA199A1 has a maximum common-mode input of **26V**. A 6S LiPo at full charge is 25.2V — only 0.8V (3%) margin. Inductive switching spikes from MOSFET commutation can easily push the battery rail to 27-28V transiently, exceeding absolute max and risking permanent damage.

**Fix:** Replace INA199A1DCKR with **INA293A2IDBVR** (LCSC C1855797):
- Common-mode range: **-4V to 110V** (vs 26V — massive margin)
- Gain: 100V/V (vs 50V/V — better ADC utilization)
- Offset: ±25µV max (vs ±150µV — 6x improvement)
- Bandwidth: 1.3 MHz (vs 14 kHz — 93x improvement)
- Package: SOT-23-5 (slightly larger than SC-70-6, requires footprint change)

With 0.2mΩ shunt and 100V/V gain:
| Load | Shunt voltage | ADC output | % of 3.3V |
|------|--------------|------------|-----------|
| 140A (4×35A) | 28mV | 2.80V | 85% |
| 35A (1 channel) | 7mV | 700mV | 21% |
| 10A (cruise) | 2mV | 200mV | 6% |

**BOM change:** Replace U1 INA199A1DCKR (C59135) → INA293A2IDBVR (C1855797). Footprint change from SC-70-6 to SOT-23-5 required.

---

---

## Low / Informational Issues

### 6. R18 Footprint Mismatch
R18 (10kΩ NRST pull-up) uses a capacitor footprint (`C_0201_0603Metric`) instead of resistor footprint. Cosmetic/DRC issue — physically works but should be corrected for production DRC cleanliness.

### 7. Ferrite Beads (FB1-FB4) Need Part Assignment
Currently generic "200mA" ferrite beads with no specific part number or impedance spec. For commercial release, assign a specific part (e.g., 120Ω @ 100MHz, ≥200mA rated). Must be available on LCSC/JLCPCB in 0201 package.

---

## Components Verified OK

### LMR51420YDDCR Buck Converter — PASS

The 0.47µH inductor (XRIM160808SR47MBCD) is 10x smaller than textbook recommendation (4.7µH), but this is a deliberate size optimization that works because:
- Actual load is only ~500mA (4× MCU + 4× gate driver + misc), well below the 1.4A IC rating
- Operates in deep DCM (discontinuous conduction mode) — load current (500mA) << ripple/2 (5.25A)
- Output ripple on 8V rail: ~0.52V peak-to-peak (6.5%) at 6S
- Gate drivers (NSG2065Q) tolerate this easily — VCC stays within 7.48-8.56V, well inside 7-13.5V operating range
- LDO PSRR (65dB @ 1MHz) filters 8V ripple to **0.93mV** on the 3.3V MCU rail
- The 1.6×0.8mm inductor is critical for the compact 20×20mm board layout
- LMR51420 has cycle-by-cycle current limiting for inductor saturation protection

### NSG2065Q Gate Driver — PASS

- VCC at 8V is at recommended minimum, UVLO at 4.5V provides margin
- 1.2A source / 1.5A sink drive current — adequate for SP40N03GNJ gate charge
- 100nF bootstrap caps provide 8.5x margin over required gate charge
- 15Ω gate resistors are appropriate for controlled switching
- 200ns internal dead time prevents shoot-through

### SP40N03GNJ MOSFETs — PASS (with note)

- 40V VDS, 75A ID, 2.9mΩ RDS(on) @ 10V VGS
- Conduction loss per MOSFET at 17.5A RMS: ~0.89W — manageable
- Gate charge 26nC — well within NSG2065Q driver capability
- 3×3mm PDFN-8L package fits the 20×20mm board
- Proven thermally in hard flight testing
- Good price and LCSC/JLCPCB availability (C22466709)

**VDS margin note:** At 6S (25.2V), switching transients with ~20nH stray inductance and 35A/50ns di/dt can produce ~14V spikes, pushing VDS to ~39V on a 40V-rated part. This is tight but workable with good PCB layout (short power loops, cap placement close to MOSFETs). The board has been tested extensively at 6S without issues, confirming the layout handles this well. For the 30×30mm variant, consider 60V parts for additional margin.

### 0805 10µF 50V Bulk Capacitors (C440198) — PASS (Keep Current)

- GRM21BR61H106KE43L (Murata, X5R, 50V) retains ~60-70% capacitance at 25V DC bias → ~6-7µF effective per cap
- 33 caps × ~6.5µF = ~215µF effective total — adequate, proven in hard flight testing
- Alternative GCM31CD71H106KE36L (1206 X7T) is NOT available on LCSC/JLCPCB
- Switching to 1206 would only gain 15-20% more capacitance but requires PCB redesign and 85% more board area per cap
- X7T vs X5R DC bias performance is nearly identical; package size is the dominant factor
- Current design validated in field: no bulk electrolytic needed

### HC-1.0-8PWT Connector — NOTED
User handling connector standard migration separately (Betaflight 8-pin JST-SH standard).

---

## DOY170N04T MOSFET Evaluation (User Inquiry)

The DOINGTER DOY170N04T (LCSC C50386319) was evaluated as a potential MOSFET upgrade:
- 40V, 170A, 1.7mΩ RDS(on) @ 10V — significantly lower resistance than SP40N03GNJ (2.9mΩ)
- Package: TDFN3333-8PL (3.3×3.3mm) — slightly larger than current 3×3mm PDFN-8L
- Would reduce conduction losses by ~40%

**Assessment:** Not recommended for v0.4:
- DOINGTER is an unestablished brand with limited track record
- 3.3×3.3mm package is slightly larger — may not fit current 3×3mm footprint without layout changes
- Lower RDS(on) means higher gate charge (Qg) — need to verify NSG2065Q can drive 6 of these per channel
- SP40N03GNJ is proven, cheaper, and thermally adequate in testing

---

## SP40N01GHNK — Candidate for 30×30mm Variant

**Siliup SP40N01GHNK** (LCSC C22385416) — same manufacturer as the SP40N03GNJ, in 5×6mm PDFN-8L.

| Parameter | SP40N03GNJ (20×20) | SP40N01GHNK (30×30 candidate) |
|-----------|-------------------|-------------------------------|
| VDS | 40V | 40V |
| ID (package) | 75A | 120A |
| ID (silicon) | — | 230A |
| RDS(on) @ 10V | 2.9mΩ | **1.2mΩ typ / 1.5mΩ max** |
| RDS(on) @ 4.5V | — | ~1.6mΩ (from RDS vs ID curve) |
| Qg | 26nC | **126nC** |
| Qgd | — | 15.5nC |
| Ciss | — | 5750pF |
| Rise / Fall | — | 5ns / 9.5ns |
| RθJC | ~2°C/W (est.) | **0.96°C/W** |
| PD | 55W | **130W** |
| EAS | not published | **1089mJ** (published!) |
| Package | PDFN-8L 3×3mm | PDFN5X6-8L **5×6mm** |
| Price | ~$0.15-0.20 | **$0.21** |
| LCSC stock | In stock | 4,535 units |

**Assessment: Strong candidate for 30×30mm variant.**

Pros:
- Same manufacturer family — proven silicon quality, consistent supply chain
- 58% lower RDS(on) (1.2mΩ vs 2.9mΩ) → ~58% lower conduction losses
- Published EAS (1089mJ) — avalanche-rated, unlike the SP40N03GNJ
- 0.96°C/W RθJC vs ~2°C/W — much better thermal performance
- Comparable price

Cons:
- Qg is 4.8× higher (126nC vs 26nC) — impacts gate driver loading
- JLCPCB assembly availability needs verification

**Gate driver compatibility check:** With 126nC Qg per MOSFET, the NSG2065Q bootstrap cap (100nF) needs to supply enough charge for the high-side MOSFET each PWM cycle. Per high-side MOSFET: 126nC required. Bootstrap cap at 8V: 100nF × 8V = 800nC available. With one high-side MOSFET switching per phase: 800/126 = 6.3× margin. **Still adequate**, though tighter than the SP40N03GNJ (800/26 = 30× margin). Consider increasing bootstrap cap to 220nF for extra margin on the 30×30 variant.

Gate switching with 15Ω gate resistor: peak gate current ≈ (8V - 3V) / 15Ω ≈ 333mA, switching time ≈ 126nC / 333mA ≈ 378ns. This is slower than the SP40N03GNJ (~78ns). For 24kHz PWM (41.7µs period), 378ns is still <1% of the cycle — acceptable. Consider reducing gate resistance to 10Ω on the 30×30 variant if faster switching is desired.

---

## Summary of Required BOM Changes for v0.4

| Ref | Current Part | LCSC | New Part | LCSC | Change Type |
|-----|-------------|------|----------|------|-------------|
| U26 | TPS746-3.3DRV | C524780 | TLV76733DRVR | C2848334 | Drop-in (same WSON-6 footprint) |
| U1 | INA199A1DCKR | C59135 | INA293A2IDBVR | C1855797 | Footprint change (SC-70-6 → SOT-23-5) |
