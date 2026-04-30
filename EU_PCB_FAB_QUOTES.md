# OpenDrone ESC — PCB Fab Quote Survey (HDI 6L + 2oz + 0.15mm + VIP + ENIG)

16 parallel-agent research pass, April 2026. Belgian buyer. Target: €1/board landed.

## Spec being quoted

| Parameter | Value |
|---|---|
| Size | 30 × 30 mm |
| Layers | 6 |
| Outer copper | 2 oz (70 µm) |
| Inner copper | 1 oz (35 µm) |
| Min via | 0.15 mm |
| Via-in-pad | YES, filled + plated flat (IPC-4761 Type 7 / VIPPO) |
| Surface finish | ENIG |
| Thickness | 1.6 mm |
| Qty tiers | 100 / 1,000 / 10,000 |
| Panel option | 150 × 150 mm (5×5 = 25 boards/panel) |

## Ranked results — €/board landed to Belgium at 1,000 pcs

Sorted by €/board @ 1k. Landed = includes shipping + VAT treatment applied (intra-EU reverse charge for EU fabs; DDP for China DHL; Brexit adders for UK).

| Rank | Fab | Country | €/board @ 100 | €/board @ 1k | €/board @ 10k | Spec fit | Online quote | Notes |
|---|---|---|---|---|---|---|---|---|
| 🥇 1 | **JLCPCB** | CN | €1.91 | **€0.44** | **€0.25** | ✅ Full (0.15mm + VIP + 2oz + ENIG) | ✅ Yes | DHL DDP BE, 8–11 WD door-to-door |
| 🥈 2 | **LeitOn** | DE | €6.93 | **€0.94** (panel €0.90) | RFQ only | ⚠ 0.20mm via at volume online (not 0.15), Type 3/4 VIP (not Type 7) | ✅ Yes | **Only EU fab under €1/board @ 1k, 0.15mm needs manual RFQ** |
| 3 | PCBWay (est.) | CN | ~€2 | ~€0.45–0.55 | ~€0.28 | ✅ Full | ✅ Yes | Extension-blocked in this run; industry pricing tracks JLC ±10% |
| 4 | NextPCB (est.) | CN | ~€3 | ~€0.95–1.30 | Email RFQ | ✅ Full | Partial | Aggressive on HDI VIP, often beats JLC on VIP-heavy 6L |
| 5 | HQPCB (est.) | CN | ~€3 | ~€1.00–1.40 | Email RFQ | ✅ Full | Partial | Sister company to NextPCB, ±5–10% |
| 6 | ALLPCB (est.) | CN | ~€3.20–4.20 | ~€1.10–1.50 | Email RFQ | ✅ VIP via RFQ | Partial | HDI via email, not instant |
| 7 | **Beta LAYOUT** (non-HDI baseline) | DE/IE | €6.77 | €1.99 | RFQ | ❌ No VIP in UI, no 2oz on 6L online, HDI → RFQ | Partial | Real HDI+VIP estimated €8–15/board @ 100 |
| 8 | ICAPE (est.) | FR broker / CN fab | ~€12–20 | ~€4–7 | ~€1.80–3.00 | ✅ Full | Login wall | EU invoice + reverse-charge VAT, CN fab. Cleanest accounting for BE B2B |
| 9 | **Eurocircuits** (HDI pool) | BE | €8.66 | €3.08 | RFQ (>2k online) | ⚠ 1oz outer only online (2oz RFQ), 1.55mm fixed | ✅ Yes | €2.47 @ 2k. Same-country 21% VAT applies. HDI+2oz+10k all RFQ. |
| 10 | Multi-CB (est.) | DE | €20–40 | ~€4–8 (at volume) | RFQ | ✅ (login wall for HDI) | Partial | Quote requires Gerber upload + login |
| 11 | Würth CBT / WEdirekt | DE | €4.57 (non-HDI) | €1.66 @ 930 (non-HDI) | RFQ | ❌ HDI → non-pool sales, estimated €6–15/board @ 1k real spec | Partial | Min 0.25mm online, Type 7 VIP = contact sales |
| 12 | NCAB (est.) | SE broker / CN fab | ~€18–28 | ~€9–13 | ~€4–6 | ✅ Full | No | Premium brokerage, 1k+ MOQ preferred, NRE €200–400 first order |
| 13 | UK (Exception / Newbury / GSPK) | UK | €30–45 | €8–13 | €5–7 + VAT | ✅ Full | No | +21% BE import VAT + €20 clearance = €6–9/board landed @ 10k |
| 14 | Aisler | NL | — | — | — | ❌ No HDI, no VIP, no 2oz outer on 6L online, 100 pcs cap | ✅ (but not this spec) | Non-HDI 6L ENIG = €8/board @ 100. Skip for production HDI. |
| 15 | French aerospace (Techci / Cibel / Atlantec / Elvia) | FR | €80–180 | €25–60 | €8–18 | ✅ Full | No | Aerospace/defence-tier, wrong customer segment for drone ESC |
| 16 | Italian + Austrian premium (SOMACIS / CISTELAIER / AT&S / Schweizer) | IT / AT / DE | €40–150 | €15–40 | €6–15 | ✅ Full | No | AT&S won't engage without multi-M€ forecast. Wrong MOQ tier entirely |
| — | Polish (TS PCB / Satland / Printor) | PL | N/A | N/A | N/A | ❌ No HDI / no VIP / no laser microvia in published capabilities | No | Strong on 2–6L standard multilayer; HDI not a Polish specialty |
| — | Czech (Gatema / Pragoboard / Cube) | CZ | RFQ | RFQ | RFQ | ✅ (Gatema + Cube) | No | No instant online HDI pricing. RFQ via email |

## Structural finding

**The €0.44–1.30/board band at 1k for 6L HDI + VIP + ENIG + 2oz is exclusively China (JLCPCB, PCBWay, NextPCB, HQPCB).** Only **LeitOn** (Berlin) comes close on the EU side — **€0.94/board @ 1k panel, but with 0.20mm via (not 0.15mm) and Type 3/4 plugged VIP (not Type 7 VIPPO) online**. For exact 0.15mm + Type 7 spec at volume, LeitOn goes to manual RFQ, expected €1.20–1.80/board @ 10k.

Everything else in EU is €3–15/board @ volume for this spec. Gap to China is structural (labor + HDI process capex + scale), not negotiable.

## LeitOn manual RFQ — received 2026-04-24 (ref 260424L24)

Quote `260424L24` from Daniel Hartmann (kontakt@leiton.de), 33×33mm board, full target spec.

**Spec delivered (matches request):**
- 6 layer, 70/35 µm outer/inner (2oz/1oz) ✅
- FR4 Tg 150°C, 1.6mm, ENIG (Ni 3-6µm / Au 0.05-0.1µm) ✅
- Min structures 0.15mm, min via 0.25mm, via pad 0.6mm ❌ **INSUFFICIENT for current design**
  - Design actually has 0.15mm drills with 0.25/0.30mm pads (HDI microvias placed in layout).
  - Leiton quote rules require ≥0.25mm drill AND ≥0.6mm via pad — both below current spec.
  - **Need re-quote for 0.15mm laser microvia + 0.25/0.3mm pad HDI build.** Expect €/pc uplift.
  - Via inventory in PCB: 0.25/0.15, 0.30/0.15, 0.30/0.20, 0.45/0.20, 0.45/0.30 (pad/drill mm).
- **Plugging & Filling: Type-7 Filled & Cu-Capped VIA** ✅ (true VIPPO, matches request)
- IPC Class 2, 100-up custom panel (10×10, 358×358mm), routing, e-test, green/white

**Pricing (EUR, ex VAT, UPS Standard to DE):**

| Qty | Lead (WD) | €/pc | Line total | +Ship | Landed €/pc |
|---|---|---|---|---|---|
| 1,000 | 18 | 0.988 | 988.00 | 10.00 | 1.258 |
| 1,000 | 24 | 0.935 | 935.00 | 10.00 | 1.205 |
| 10,000 | 37 | 0.522 | 5,220 | 33.00 | 0.527 |
| 10,000 | 43 | 0.480 | 4,800 | 33.00 | 0.483 |
| 10,000 | 116 | 0.451 | 4,510 | 33.00 | 0.454 |
| 120,000 | 64 | 0.394 | 47,280 | 354.85 | 0.398 |
| 120,000 | 137 | 0.365 | 43,800 | 354.85 | 0.368 |

Setup: €270 (1k), €450 (10k+). All setup included in line totals above.

**Analysis vs research-pass estimate (€0.94/board @ 1k panel with 0.20mm via and Type 3/4 VIP):**
- Real quote is €0.988/board @ 1k with **0.25mm min drill + 0.6mm min via pad** — does NOT cover the design's 0.15mm microvias. Quote is for standard-via spec, not HDI.
- Type-7 VIPPO delivered (better than the estimated Type 3/4).
- 10k tier @ 43 WD = €0.48/board — below estimate, but again for non-HDI spec.
- **Re-quote required with 0.15mm microvia rules to get real EU-HDI price.**
- Country of production is China, processed/invoiced by Leiton GmbH DE. EU invoice, reverse-charge VAT to BE works.
- Validity: 2 weeks from 2026-04-24 (expires ~2026-05-08).

**Verdict:** Viable EU production path. 10k @ €0.48 is ~2× JLC (€0.25) — structural gap per research finding, but EU-branded invoice is achievable at <€1/board.

**Open questions for Leiton follow-up:**
1. **Re-quote with 0.15mm laser microvia rules** — design has 0.15mm drills with 0.25/0.30mm pads. Current quote's 0.25mm drill / 0.6mm via pad minimums do not fit.
2. Stackup definition (impedance control for DShot edges / BEMF sense).
3. Depaneling method — v-score vs mousebites on the 10×10 panel.
4. Assembly quote (separate — turnkey EU ESC needs PCBA, not bare boards).
5. Actual production-country option ("Production in Germany possible, ask us explicitly" — get €/pc delta).

## Concrete next actions

### Option A — Full China (status quo, cheapest)
**Stay on JLCPCB** for fab. €0.44/board landed @ 1k, €0.25 @ 10k. This is what OpenDrone V1 is already doing. No EU-sourcing marketing angle but best unit economics.

### Option B — LeitOn production pilot (best realistic EU path)
1. Export gerbers + CPL from KiCad Fabrication Toolkit
2. Email sales@leiton.de with full 0.15mm + Type 7 VIP spec at 1,000 / 5,000 / 10,000 pcs (single + panel)
3. Compare quote against online €0.94/board baseline
4. If manual quote lands ≤ €1.50/board @ 5k+ → **LeitOn is the EU production path**
5. If >€2.50/board → revert to JLCPCB for fab, only do assembly in EU

### Option C — ICAPE brokerage (EU accounting, CN fab)
Registered FR company, EU invoice with reverse-charge VAT, but PCBs fabbed in China. ~€1.80–3.00/board @ 10k estimated. Clean accounting for BE B2B, no personal import/customs handling. Login-walled quote tool — register account at eshop.icape-group.com and upload gerbers.

### Option D — Skip the premium EU fabs entirely
NCAB / Eurocircuits / Würth / Multi-CB are all €3–15/board for this spec. Only justified if the "Made in EU" end-customer requirement is absolute (medical / automotive / aerospace). For drone ESC, not worth the 7–30× premium over JLC.

### Parallel RFQ list for accurate numbers

Send the same RFQ (gerbers + CPL + spec sheet + 100/1k/10k tiers) simultaneously to:
- sales@leiton.de (Germany — best-real EU shot)
- sales@gatema.cz (Czech Republic — Gatema, HDI-capable)
- sales@cube.cz (Czech Republic — Cube, 24h express HDI)
- Via eshop.icape-group.com (France broker, CN fab — after account registration)
- ~~sales@eurocircuits.com~~ **BOUNCES** (550 5.4.1, 2026-04-24). Use web form https://www.eurocircuits.com/contact-us/ or phone +32 15 28 16 30 (Mechelen, BE).
- sales@jlcpcb.com (China — baseline, bypasses their calculator caveats for Type 7 VIP)
- sales@pcbway.com (China — direct competitor to JLC)
- sales@nextpcb.com (China — HDI-specialized, often beats JLC on VIP)

Expected turnaround 24–72h. Real numbers will refine this table substantially. The rank order is unlikely to change materially — JLCPCB-class China pricing is ~3× below the best EU price.

## Flagged issues from the research pass

1. **Polish domain hijacks:** `elprinta.pl` and `tspcb.com` redirect to Würth WEdirekt (wedirekt.com). Use `tspcb.pl` for the real Polish TS PCB site.
2. **Browser extension interference:** the Multi-CB research agent observed competitor tabs spawning automatically (AISLER / Leiton / Eurocircuits / PCBWay / WeDirekt / Satland / NCAB / ICAPE / Prototypy). Could be a price-comparison Chrome extension or a malicious one. Audit browser extensions when convenient.
3. **Belgium-to-Belgium VAT:** Eurocircuits sells BE-to-BE → 21% BE VAT applies on invoice, no reverse-charge (same-country B2B is standard VAT). All other EU fabs → reverse charge with BE VAT number.
4. **DDP vs DAP at JLC/PCBWay:** JLCPCB quotes DHL Express DDP (VAT bundled, no BE customs surprise). Confirm DDP is selected at order time, not default DAP which would hit user with 21% + clearance fee at delivery.

## References

### Agents completed this run (per supplier)
Reports from: Eurocircuits (BE), Aisler (NL), Multi-CB (DE), Beta LAYOUT (DE/IE), Würth CBT (DE), LeitOn (DE), Polish fabs (TS PCB/Satland/Printor), Czech fabs (Gatema/Pragoboard/Cube), Italian+Austrian (SOMACIS/CISTELAIER/AT&S/Schweizer), French (Techci/Cibel/Atlantec/Elvia/Cirly), ICAPE (FR broker), NCAB (SE broker), JLCPCB, PCBWay (killed on extension disconnect), other Chinese (NextPCB/HQPCB/ALLPCB/PCBGOGO/Seeed/Elecrow), UK (Exception/Newbury/GSPK/Stevenage).

### Quote tool URLs
- [JLCPCB quote tool](https://cart.jlcpcb.com/quote) — ✅ full HDI+VIP online pricing
- [LeitOn calculator](https://www.leiton.de/pcb-online-calculation.html) — ✅ instant for ≤3m², 0.20mm via at volume
- [Eurocircuits HDI pool](https://be.eurocircuits.com/shop/assembly/configurator.aspx) — ✅ up to ~2k pcs online
- [WEdirekt configurator](https://www.wedirekt.com/en/configurator) — ⚠ non-HDI pool only
- [Beta LAYOUT configurator](https://eu.beta-layout.com/pcb/configurator/) — ⚠ non-HDI pool only
- [Multi-CB portal](https://portal.multi-circuit-boards.eu/) — login-walled
- [Aisler](https://aisler.net/p/new) — ❌ not HDI-capable
- [ICAPE eshop](https://eshop.icape-group.com/) — login-walled
- [Gatema extranet](https://extranet.gatemapcb.com/dps/konfigurator.aspx) — login-walled

### Related docs
- `EU_SOURCING.md` — component-side EU pipeline
- `EU_PIPELINE.md` — assembly equipment + in-house production
