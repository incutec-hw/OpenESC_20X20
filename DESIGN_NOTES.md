# Design Notes

Engineering notes mirrored from the on-canvas comments in the KiCad schematic
(`4in1-mini.kicad_sch`, `ESC.kicad_sch`). This file is the human-readable copy of
the design rationale annotated directly on the sheets — keep the two in sync.

> This is the **20×20** (mini) OpenESC. The
> [OpenESC-30x30](https://github.com/incutec-hw/OpenESC-30x30) (30.5×30.5 mm) shares
> this design and carries the same notes; the two differ only in board/mounting size
> and a few power-stage parts (MOSFET, TVS, shunt count). The 30×30 canvas carries
> additional buck/TVS/decoupling annotations that apply to both boards.

---

## Main sheet (`4in1-mini.kicad_sch`)

**Topology:** +BATT input, TVS clamp, buck + LDO power, board-level current sense, 8-pin connector.

### Input protection
- 2× **SMF24A-T13** TVS on +BATT (24 V standoff). 6S-only target.

### Buck (gate-drive rail)
- **LMR54406DBVR**: 4–36 V input, 1.1 MHz, 0.6 A — plenty for gate driving.
- FTC160808S4R7MBCA 4.7 µH inductor. FB divider 115k / 10k, Vref 0.8 V → **10.0 V** rail.

### Current sense
- Board-level high-side: **0.2 mΩ shunt × 100 V/V (INA186A3) gain → Max 165 A** at 3.3 V ADC.

---

## Per-channel ESC (`ESC.kicad_sch`)

**Topology:** a single ESC channel, duplicated 4×. One AT32 MCU + one NSG2065Q gate
driver + 6 MOSFETs (low and high side per phase).

- **Microcontroller:** AT32 (AT32F421G8U7). Flashed via SWC.
- **Gate driver:** NSG2065Q — gate driver has an integrated diode.
- **MOSFETs:** DOY180N03T, low and high side for each phase.
- **Bootstrap capacitors** for high-side N-MOS switching.
- **BEMF feedback network** for sensorless commutation.
- **LPF on VDDA** (MCU analog supply).
