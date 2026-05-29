# Open 4-in-1 AM32 ESC

An open-source 4-in-1 ESC for FPV drones. Runs [AM32](https://github.com/AlkaMotors/AM32-MultiRotor-ESC-firmware) firmware, works with Betaflight over DShot. Designed in KiCad.

I made a video explaining how it works: https://www.youtube.com/watch?v=TwAmmPxOpTM

<img width="622" height="678" alt="Screenshot 2026-03-09 at 21 01 59" src="https://github.com/user-attachments/assets/40ab86d7-e7c2-46e8-b2fc-61c8ba19fa80" />
<img width="604" height="640" alt="Screenshot 2026-03-09 at 21 02 12" src="https://github.com/user-attachments/assets/c0d8b194-cb31-4f07-9650-9fd69ad4cd7d" />

## Specs

| Parameter | Value |
|---|---|
| Firmware | AM32 |
| Input voltage | 3-6S LiPo (11.1-25.2V) |
| Continuous current | 35A per channel |
| MCU | AT32F421G8U7 (ARM Cortex-M4, 120MHz) |
| Gate driver | NSG2065Q (3-phase, FD6288Q-compatible) |
| MOSFETs | SP40N03GNJ (40V, 2.9mΩ) — optional FDMC8010DC (30V, 1.28mΩ) for premium builds |
| Current sensing | INA186A3IDCKR (100V/V) + 0.2mOhm shunt (165A max) |
| Protocol | DShot (Betaflight compatible) |
| Power supply | LMR51420YDDCR buck + TLV76733DRVR LDO |
| Connector | JST SM08B-SRSS-TB (Betaflight 8-pin standard) |
| PCB | 6-layer, 1oz copper |

## Alternative Components

The gate driver footprint is compatible with the entire FD6288Q clone family (27,000+ units combined stock across 7+ manufacturers) and the TI DRV8300. No PCB changes needed for any of them. Multiple pin-compatible MOSFET options are also available, including the FDMC8010DC (30V, 1.28mΩ) as a premium low-resistance option — 36% lower total phase resistance at the cost of reduced voltage headroom (7S max vs 8S+) and higher per-unit cost.

See [ALTERNATIVES.md](ALTERNATIVES.md) for the full list of pin-compatible gate drivers and MOSFETs with LCSC part numbers, specs, and stock levels. Design rationale (dead time, Vds margin, commutation loop, BEC stage, bring-up) is in [DESIGN_NOTES.md](DESIGN_NOTES.md).

## How it's built

The schematic is split into a main sheet and a sub-sheet that's reused 4 times — one per ESC channel.

The main sheet (`4in1-mini.kicad_sch`) has the power supply, current sensing, and the 8-pin connector. Each ESC channel (`ESC.kicad_sch`) has:
- AT32F421G8U7 running AM32 firmware
- NSG2065Q 3-phase gate driver with bootstrap caps
- 6x SP40N03GNJ MOSFETs in 3 half-bridges
- Back-EMF feedback network for sensorless commutation

## Project structure

```
4in1-mini.kicad_sch   Main schematic (power, sensing, connector)
ESC.kicad_sch         Single ESC channel (used 4x)
4in1-mini.kicad_pcb   PCB layout
4in1ESC.pretty/       Custom footprints
4in1ESC.3dshapes/     3D models (STEP files)
components.kicad_sym  Custom symbols (gate driver, connector, etc.)
datasheets/           Component datasheets
licensing/            Branding and third-party notices
tools/                Analysis scripts
```

## License

Licensed under [CERN-OHL-S-2.0](https://ohwr.org/cern_ohl_s_v2.txt). See [LICENSE](LICENSE) and [licensing/](licensing/) for branding and third-party notices.
