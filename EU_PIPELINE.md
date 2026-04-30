# OpenDrone — EU Production Pipeline (Belgium)

Full EU supply + in-house assembly pipeline for OpenDrone ESC production, targeting **<€20K capex** and high-current multi-layer PCBs.

---

## 0. Honest constraint first

**Multi-layer PCB fabrication in-house is not feasible at €20K capex.** Pro multilayer fab (4-layer, 2oz copper, PTH, solder mask, ENIG finish) needs €100K+ in equipment: lamination press, drilling CNC, copper plating line, etching line, solder mask exposure, reflow. You CAN etch single-sided prototypes on a €1K CNC/LPKF but that's useless for a 4-in-1 ESC.

**The real EU pipeline is: outsource fab to an EU fab house (Eurocircuits is in Belgium), do assembly in-house.** This is what every European prototype-to-small-series EMS actually does. Plan below reflects that.

---

## 1. Pipeline Overview

```
┌────────────────────────────────────────────────────────────────────┐
│  BOM sourcing → PCB design → Fab (EU) → Stencil (EU) → Components  │
│    (Mouser/Farnell EU)              (Eurocircuits BE, same country) │
│                                                                     │
│  → PASTE PRINT → PICK & PLACE → REFLOW → INSPECT → TEST → PACK      │
│        (all in-house, sub-€20K equipment)                          │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. PCB Fabrication — Outsourced to Belgium

### Chosen fab: **Eurocircuits** (Mechelen, BE)

- Same country → no VAT export hassle, 1-day shipping
- Supports 2oz / 70µm copper on outers (high-current OK) + inner 1oz
- Up to 8 layers standard, 4 layers ideal for 4-in-1 ESC
- ENIG finish supported (gold plating over nickel, best for fine-pitch ICs)
- Prices: ~€50–150 for 5 pcs 4-layer 100×100 mm 2oz; ~€2–5/board at 100+ pcs
- **STENCIL included or separate order** (framed or frameless, ~€30–70 per stencil)
- Lead time: 3–5 days standard, 24h express (+50% cost)

### Alternative EU fabs (in order of preference for Belgium)

| Fab | Country | Strengths | Notes |
|---|---|---|---|
| **Eurocircuits** | BE | Same country, fast, quality | **Primary** |
| Aisler | NL | Faster bring-up, good UI | Higher cost at volume |
| Multi-CB | DE | Mid-volume pricing | Longer lead from BE |
| Würth Elektronik CBT | DE | Top quality, automotive-grade | Expensive |
| Elprinta / PCBCart EU | Various | Backup | Less proven for low-volume |
| ICAPE Group | FR | Volume (500+ pcs) | Factory in Asia + EU warehouse |

### Stackup recommendation for 4-in-1 ESC (high-current)

```
L1 — 2oz (70µm) copper — signal + high-current phase pours
L2 — 1oz inner — ground plane
L3 — 1oz inner — power distribution (VBAT, 3.3V, 5V, VDRV)
L4 — 2oz (70µm) copper — signal + high-current return
Total thickness: 1.6 mm standard
```

Eurocircuits **cannot do asymmetric copper** (e.g. 2oz on L1 only). If cost is priority, drop to 1oz outer + 1oz inner (4× cheaper) and use wider traces + more vias for current.

### Files to send

- Gerber X2 or RS-274X (KiCad 9 native export via Fabrication Toolkit)
- Excellon drill file
- Pick-and-place file (CPL) — for stencil alignment & our P&P
- BOM — IPN + MPN + footprint

---

## 3. In-House Assembly Workflow

```
     Fabbed PCBs arrive from Eurocircuits
            │
            ▼
     Apply stencil + print solder paste  (Paste printer)
            │
            ▼
     Pick & place all SMT components     (Pick & place machine)
            │
            ▼
     Reflow solder profile               (Reflow oven)
            │
            ▼
     Visual + optical inspection         (Stereo microscope / AOI)
            │
            ▼
     Hand-solder through-hole            (Iron + fume extractor)
            │
            ▼
     Functional test                     (ICT jig + power supply)
            │
            ▼
     Clean + package                     (Ultrasonic + ESD bags)
```

---

## 4. Equipment List & Budget (Target: <€20K total)

Three tiers depending on volume ambition. All prices ex-VAT, new unless noted, EU-sourced.

### Recommended: Neoden line via NL distributors + BE/DE accessories (~€18.5K)

Single-vendor simplicity, 2-year warranty, NL-stocked spares, 1–2 week lead to Belgium, no post-Brexit customs exposure, intra-EU reverse-charge VAT.

| Item | Vendor (URL) | Country | Model | Price ex-VAT (€) |
|---|---|---|---|---|
| Pick & place | **Printtec** (printtec.nl) | NL | Neoden 4 + extra feeders, **2-yr warranty explicit** | 9,500 |
| Reflow oven | **NeoDen Tech Europe** (neodentech.eu) | NL | Neoden IN6C (6-zone convection, nitrogen-capable on C variant) | 3,500 |
| Stencil printer | NeoDen EU | NL | Neoden manual stencil printer + frame | 700 |
| Soldering station | **Farnell BE** (be.farnell.com) | BE | JBC CD-2BE (or CD-1BQF) | 450 |
| Stereo microscope | **Euromex** (euromex.com) | NL | NexiusZoom 6.7×–45× + LED ring | 1,100 |
| Dry cabinet (JEDEC MSL) | **Totech Europe** (totech.eu) | NL | 150–250 L Super Dry | 2,000 |
| ESD workbench + mat + wrist strap + chair | **esd.equipment** (DE) | DE | 1.8 m Treston bench kit | 900 |
| Consumables starter (paste, flux, cleaner, tweezers, trays, nozzles) | **TME** (tme.eu) + Farnell BE | PL + BE | — | 300 |
| **Total** | | | | **~€18,450** |

Total order-to-running-line: **2–4 weeks**. Shave ~€450 by dropping to Neoden 3V or using a used stencil printer to land firmly under €18K.

**Skip AOI year 1** — nothing new in EU under €5K. Add used Mek (NL) or Koh Young via AdoptSMT once volume justifies it (year 2+).

### Budget alternative (~€8K) — Neoden entry + Puhui/Elektor oven

| Item | Vendor | Model | € |
|---|---|---|---|
| Pick & place | Printtec / NeoDen EU | Neoden 3V (entry, 2-yr warranty) | 4,500 |
| Reflow oven | **Elektor** (elektor.com) | Puhui T-962 v2 "Elektor Version" (EU consumer warranty) | 250 |
| Stencil printer | NeoDen EU | Neoden manual | 700 |
| Soldering station | Farnell BE / TME | Hakko FX-888D | 130 |
| Microscope | eBay DE | Used Nikon SMZ-1B + LED | 400 |
| Dry cabinet (small) | Totech EU | 60–100L entry | 800 |
| ESD bench basics | esd.equipment / Manutan BE | mat + strap + chair | 350 |
| Consumables | TME + Farnell BE | — | 300 |
| Fume extractor | Farnell BE | Weller Zero Smog 4V | 450 |
| **Total** | | | **~€7,880** |

Tier-A equivalent. Good for 10–50 boards/month. Upgrade reflow oven first when volume justifies (T-962 is fine for bring-up, bad for a production line — real 6-zone convection Neoden IN6C @ €3.5K is the right next step).

### Second-hand pro route (~€15–20K, if you want industrial capacity)

Via **AdoptSMT** (adoptsmt.com, AT/DE/PL), **allSMT** (allsmt.com, Monschau DE — near BE border), **Exapro** (EU marketplace), **KVMS** (kvms.be, Turnhout BE — local Belgian SMT/SEHO/Wertheim reseller).

| Item | Used target | Typical EU € |
|---|---|---|
| Pick & place | Yamaha YV100XG, Juki KE-2050/2060, Mydata MY9/MY12 (2005–2015) | 8–15K |
| Stencil printer | DEK Horizon 01i, MPM UP1500 | 3–5K |
| Reflow oven | BTU Pyramax 75N, Heller 1707 EXL, Rehm VisionX | 3–6K |
| AOI | Viscom S3088, Mek, Koh Young (rare under €10K) | 4–10K |

**Caveats**: pro equipment needs **400V 3-phase power**, ~6 bar compressed air, proper floor space + loading dock or ground-floor access, spare parts network, refurb skill. Refurb warranty is typically 3–6 months only. **Only pursue if you're committed to ≥500 boards/month steady state.**

---

## 5. Belgian / EU Logistics Details

### Where to buy equipment (verified EU distributors, closest to Belgium first)

**Pick & place / reflow / stencil (Neoden line) — primary path:**
- **Printtec** (NL) — printtec.nl — authorized Neoden reseller with explicit 2-year warranty. Primary vendor.
- **NeoDen Tech Europe** (NL, Geldermalsen) — neodentech.eu — spares + full Neoden range, backup vendor
- **ESD Shop EU** (SK/CZ) — esdshop.eu — secondary Neoden reseller

**Local Belgian industrial SMT:**
- **KVMS** (Turnhout, BE) — kvms.be — sells SMT Wertheim / SEHO / Nordson. For future industrial scale-up; also local service.

**Used industrial SMT (Yamaha/Juki/DEK/BTU/Heller):**
- **AdoptSMT** (AT/DE/PL) — adoptsmt.com — refurb warranty typically 3–6 months
- **allSMT** (Monschau DE, near BE border) — allsmt.com
- **Exapro / Kitmondo / Machinio** — EU marketplaces, seller-dependent warranty
- **Werktuigen.nl** (NL), **Surplex.com** (DE), **Maschinensucher.de** — general used industrial
- **eBay DE/IT** — business-seller listings only

**Dry cabinet / ESD bench / microscope:**
- **Totech Europe** (NL) — totech.eu — JEDEC MSL dry cabinets, industry standard
- **XDry Europe** — xdry.com — alternative dry cabinet supplier
- **Euromex Microscopen** (NL, Duiven) — euromex.com — NexiusZoom + StereoBlue stereo microscopes
- **esd.equipment** (DE) — esd.equipment — Treston ESD benches
- **Manutan BE** — workshop furniture basics (NOT ESD-critical)

**Consumables + soldering tools:**
- **TME** (PL) — tme.eu — JBC/Hakko/Weller/Metcal full range, aggressive EU pricing
- **Farnell / element14 BE** — be.farnell.com — overnight BE delivery, Belgian VAT
- **Distrelec BE** — distrelec.be — industrial
- **Reichelt** (DE) — reichelt.com — Weller + Ersa strongest
- **Welectron** (DE) — welectron.com — low-volume hobby/pro gear

**PCB fab (since you're going JLC for production, these are backup only):**
- **Eurocircuits** (BE, Mechelen) — stable per 2026 research, Avedon Capital growth investment Feb 2026
- **Aisler** (NL) — fast prototype turn
- **Multi-CB** (DE) — aggressive pricing mid-volume
- **Beta LAYOUT / PCB-POOL** (DE) — also sells reflow kits + stencils

### Avoid for a Belgian production line

- **Eleshop** — doesn't carry Neoden/CharmHigh/Puhui at production grade (earlier assumption was wrong)
- **CharmHigh via Amazon/AliExpress/RobotDigg** — no EU reseller, no warranty, no spares path. Grey import.
- **UK vendors** (Etek Europe, AMS Electronics, Kaisertech) — post-Brexit customs kills economics for BE. Use NL/DE equivalent.
- **Opulo LumenPnP for production use** — EEVblog reports of bricked mainboards, bad sensorless homing, feeder overheating. Fine as hobby project, not a production line.
- **Puhui T-962 as production reflow** — modded toaster. OK for bring-up/prototypes, not a product line. Neoden IN6C is only ~€3K more and is real convection.
- **"JLCPCB EU warehouse" / "PCBWay EU" as fab alternatives** — PCBs are still made in China; EU warehouse only stocks modules. Not equivalent to EU fab.
- **Foeth.com** — sells chemical/pharma/food process equipment, not SMT. Ignore.

### Component sourcing (matches EU_SOURCING.md)

- **Mouser EU** (warehouse DE Munich) — primary
- **Farnell / element14 BE** — Belgian warehouse
- **DigiKey EU** (warehouse DE) — fast shipping
- **Avnet Silica BE** — Infineon / ST volume
- **EBV BE** — Nexperia / NXP volume
- **Rutronik** — Infineon volume

All ship to Belgium with intra-EU VAT reverse charge (no VAT on invoice for B2B with VAT number, accounted on BE VAT return).

### Consumables (ongoing, not capex)

| Item | Brand | Source | €/unit |
|---|---|---|---|
| Solder paste | **Indium 8.9HF** or AIM M8 (SAC305, no-clean) | Farnell / Almit EU | 50–80/500g |
| Stencils | Framed or frameless, 0.12 mm steel | Eurocircuits (include with PCB order) | 30–70 |
| Flux (pen + gel) | Amtech NC-559, MG Chemicals | TME / Farnell | 10–30 |
| Cleaning solvent | Techspray Flux Remover | Farnell | 15 |
| ESD bags | Desco, Kolibri | Farnell / Manutan | 0.10/bag |
| Isopropanol 99% | Bulk (1L–5L) | Conrad / TME | 10–30 |
| Nitrile gloves | — | Manutan | 20/box |

Plan ~€200–500/month consumables for small-series production.

---

## 6. Workspace Requirements

### Minimum room spec

- **15–25 m²** floor area
- 3× 230V single-phase outlets (reflow oven, P&P, soldering)
- Good ventilation (fume extractor exhaust routing — window or ducted)
- ESD flooring or ESD mats over existing floor
- Temperature 18–25°C, humidity 30–70% (dry cabinet handles MSL)
- No carpet (static)

### Pro setup adds

- 400V 3-phase if Tier C equipment (Yamaha/BTU oven)
- Compressed air (6 bar) for stencil printer + P&P feeders (some models)
- ESD-grade flooring (conductive vinyl, ~€30–60/m²)

### Compliance

- **CE marking self-declaration** — OpenDrone products need Declaration of Conformity, RED + EMC (EN 55032 / EN 301 489) if RF, LVD + EMC otherwise. Test lab visit ~€2–5K for pre-compliance, skip if hobby-grade.
- **RoHS** — all BOM components must be RoHS-compliant (Mouser/Farnell filters default to this, trivial to comply)
- **WEEE registration** — BE WEEE registration via **BeWeee / Recupel** for putting electronics on the BE market. ~€200/yr + fee per kg.
- **FCC** — not required for EU sales. US export only.
- **Belgian VAT + intra-EU B2B** — reverse charge simplifies component imports; OSS (One-Stop Shop) for B2C EU sales.

---

## 7. Volume Economics & Scaling

### Rough per-unit cost breakdown for V2 EU ESC (Tier B in-house, 100-unit run)

| Cost category | € per unit | Notes |
|---|---|---|
| PCB (Eurocircuits 4L 2oz @ 100 qty) | 4–7 | 70×70 mm board |
| Stencil amortized | 0.5 | €50 stencil / 100 boards |
| Components (BOM @ Mouser/Farnell, 10k price) | 15–22 | See EU_SOURCING.md V2 BOM |
| Paste + flux + consumables | 0.8 | |
| Labor (self, @ €30/h, 0.5 h/board) | 15 | Or €0 if hobby |
| Reject/rework overhead (5%) | 1 | |
| **Sub-total BOM + assembly** | **~€37–46** | Before margin |
| **vs JLCPCB assembled V1** | ~€20–25 | LCSC sourcing |

EU pipeline is **~2× the unit cost of JLCPCB** — consistent with "premium EU SKU" positioning.

### Break-even volume for Tier B capex (€18K)

Assuming €20–30 gross margin per V2 ESC: **600–900 units to amortize equipment**. Below that, outsource to an EU EMS (Eurocircuits Assembly, Aisler Assembly, Multi-CB, PCBWay EU) instead of buying machines.

---

## 8. Recommended Workflow & First Build

### Phase 1 — Validate pipeline with V1 AT32 design (now)

1. Export Gerbers from KiCad via Fabrication Toolkit
2. Order 5 pcs + stencil from **JLCPCB** (existing pipeline, cheapest fab path)
3. Order full BOM from Farnell BE (1-day delivery) or TME (PL, aggressive pricing)
4. Hand-assemble 1 board using borrowed/rented Tier A-equivalent tools
5. Validate entire flow end-to-end before buying machines

PCB fab stays on JLCPCB for V1 production economics. Only consider EU fab (Eurocircuits/Multi-CB) for V2 premium SKU where the "full EU supply chain" marketing story is the point, or for fast-turn prototyping where JLC shipping is the bottleneck.

### Phase 2 — Buy Tier B equipment (€18K)

Only after Phase 1 proves the pipeline works.

Order sequence to minimize idle capital:
1. Pick & place + reflow (core productivity) — 30 day lead for Neoden K1-S
2. Stencil printer + AOI (quality gate) — once P&P arrives
3. Storage + consumables (ongoing top-up)

### Phase 3 — Production OpenDrone ESC V1 EU runs (3–6 months post-launch)

Start with 50 boards/month. Iterate the jig / test setup. Refine reflow profile for Infineon source-down (higher thermal mass under pad).

### Phase 4 — Transition to V2 premium SKU (when C5 + AM32 port + source-down OptiMOS align)

Same pipeline, new BOM. Paste profile may need retuning for 3.3×3.3 source-down (different paste aperture geometry).

---

## 9. Parallel Path — Contract EU Assembly (if in-house stalls)

Keep this in back pocket. All work from the same Gerbers + BOM + CPL:

- **Eurocircuits Assembly** (BE) — same-house PCB + assembly, turnkey, ideal for V2 pilots. ~€200–500 setup + €3–10/board at 50–100 qty.
- **Aisler Assembly** (NL) — fast turn, small MOQ, higher unit cost
- **Multi-CB / Beta LAYOUT Assembly** (DE) — mid-volume (100–1000)
- **PCBWay EU turnkey** — leverages their parts library, may have more of our BOM in stock than EU assemblers

Use these while building V1 EU supply chain, before committing to Tier B capex.

---

## 10. Capex Summary

| Path | Capex | Throughput | V1 start | V2 premium |
|---|---|---|---|---|
| **Tier A (proto)** | €8K | 10–100/mo | ✅ | ⚠ tight |
| **Tier B (recommended)** | €18K | 100–500/mo | ✅ | ✅ |
| Tier C (used pro) | €18K | 500+/mo | ✅ | ✅ (risk) |
| Outsource to EU EMS | €0 capex, €3–10/board | Unlimited | ✅ | ✅ |

**Recommended: start Phase 1 (outsource) → buy Tier B after validating demand.**

---

## 11. Action Items

- [ ] Get a quote from Eurocircuits for V1 AT32 ESC: 10 pcs + stencil + BOM assembly (full turnkey) to benchmark against DIY pipeline
- [ ] Identify workshop space (15–25 m²) with 230V + ventilation + no carpet
- [ ] Register BE VAT number if not already done (required for B2B reverse charge on Mouser/Farnell EU)
- [ ] Register with **Recupel** for BE WEEE compliance
- [ ] Request quotes from Eleshop NL for Neoden K1-S + Puhui T-962C+ + AOI Mini bundle (Tier B core)
- [ ] Join CharmHigh / Neoden / LumenPnP user communities for operational tips before buying
- [ ] Prototype V1 build using Tier A tools before committing to Tier B capex
- [ ] Decide: buy stencil from Eurocircuits with each PCB order (stays cheap) vs in-house stencil cutter (LPKF — way over budget, skip)

---

## 12. Open Questions for Stan

1. Target monthly volume at steady state? (100? 500? 1000?) — drives Tier A vs B vs C
2. Available workshop space + power? (230V single-phase only, or 400V 3-phase available?)
3. Solo operation or will there be an assistant at some point? (P&P machine time is not free — each board takes 1–5 min on Tier B)
4. First-year volume estimate for V1 sales? (determines break-even math)
5. Would a shared EMS arrangement with Alka or other AM32 hardware folks lower shared capex? (joint investment in Tier C equipment)

---

## 13. References

### PCB fab
- [Eurocircuits (BE Mechelen)](https://www.eurocircuits.com/)
- [Eurocircuits 2025 retrospective](https://www.eurocircuits.com/eurocircuits-company-update/looking-back-at-2025/)
- [Avedon Capital investment Feb 2026 (Evertiq)](https://evertiq.com/news/2026-02-05-eurocircuits-brings-in-avedon-capital-partners-to-support-next-growth-phase)
- [Aisler (NL)](https://aisler.net/)
- [Multi-CB (DE)](https://www.multi-circuit-boards.eu/)
- [Beta LAYOUT / PCB-POOL (DE)](https://uk.beta-layout.com/)

### Assembly equipment — EU distributors (verified)
- [Printtec (NL) — Neoden authorized, 2-yr warranty](https://printtec.nl/contents/en-uk/d596_Neoden-pick-and-place-machines.html)
- [NeoDen Tech Europe (NL, Geldermalsen)](https://www.neodentech.eu/)
- [ESD Shop EU (SK/CZ)](https://www.esdshop.eu/osadzovaci-automat-neoden/)
- [KVMS (Turnhout BE) — industrial SMT reseller](https://kvms.be/products/smt/)
- [AdoptSMT (AT/DE/PL) — used SMT](https://www.adoptsmt.com/en/)
- [allSMT (Monschau DE)](https://www.allsmt.com/?lang=eng)
- [Exapro — used P&P marketplace](https://www.exapro.com/c651-pcb-pick-and-place-machines/)
- [Autotronik-SMT (DE, Amberg)](https://autotronik-smt.de/en/)
- [Elektor — Puhui T-962 v2 EU consumer warranty](https://www.elektor.com/products/upgraded-t-962-v2-reflow-soldering-oven-elektor-version)
- [Mek Europe BV (NL Tilburg) — AOI/SPI](https://marantz-electronics.com/)
- [Totech Europe (NL) — JEDEC dry cabinets](https://www.totech.eu/dry-cabinets/)
- [Euromex (NL) — stereo microscopes](https://www.euromex.com/en/products/products/stereo-microscopes/)
- [Treston ESD benches via esd.equipment (DE)](https://esd.equipment/en/arbeitsplatzsysteme/treston.html)

### Consumables + tools
- [TME (PL)](https://www.tme.eu/)
- [Farnell BE](https://be.farnell.com/)
- [Distrelec BE](https://distrelec.be/)
- [Reichelt (DE)](https://www.reichelt.com/)

### Compliance / regulatory
- [Recupel (BE WEEE compliance)](https://www.recupel.be/)

### Reference / do NOT use for production
- [Opulo LumenPnP](https://www.opulo.io/) — hobby only; EEVblog has production issues
- [CharmHigh](https://www.charmhigh-tech.com/) — no EU reseller
- [Puhui direct](https://www.puhuitech.com/) — no EU reseller (use Elektor rebrand only)
- [T-962 retrofit mods](https://github.com/UnifiedEngineering/T-962-improvements) — for the Elektor T-962 v2 bring-up only

---

## 14. Related docs

- `EU_SOURCING.md` — component-side EU pipeline (distributors, BOM alternatives)
- `ALTERNATIVES.md`, `SOURCE-DOWN-OVERVIEW.md` — MOSFET/gate driver supply analysis
