# Research log: solder balls on Al top metal

Work-in-progress notes. Raw findings land here first and are then written up
in `docs/`. Claims are only as good as the linked source; items marked
**(unverified)** still need a primary source.

## 1. The starting point: GF180MCU pads

- GF180MCU I/O library bond pad opening is 60 um x 60 um; I/O cell is about
  350 um tall including the pad.
  <https://gf180mcu-pdk.readthedocs.io/en/latest/IPs/IO/gf180mcu_fd_io/features.html>
- PDK minimum pad opening is 40 um, minimum opening to opening spacing 9 um
  (defaults are "for DRC only", the assembly house sets real values).
  <https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_1.html>
- Top metal thickness options in the docs are 6 kA, 9 kA and 11 kA; 6 kA is not
  recommended for Cu wire bonding.
  <https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_2.html>
- The design manual has pad rule variants for wedge bond, ball bond and gold
  bump, plus top metal (TM.x) rules that mention bump pad / UBM opening.
- TODO: confirm which metal stack and top metal thickness wafer.space uses, die
  sizes, and whether parts ship as bare diced die. **(unverified)**

## 2. Electroless Ni/Au on Al via zincation (first pass)

- Sequence: alkaline Al clean, zincate, (nitric strip, second zincate),
  electroless Ni, immersion Au. Double zincate is reported as needed for best
  adhesion; second cycle recommended when Al is thicker than about 0.5 um.
  <https://www.uyemura.com/under-bump-metallization-to-reduce-wafer-processing-costs.htm>
- A process aimed at plating Al bond pads on individual ICs exists in the
  literature, including autocatalytic Au on top for stud bumping / wire bonding.
  <https://www.electronics.org/system/files/technical_resource/E8%26S33_02.pdf>
- Patent US 6548327, "Low cost electroless plating process for single chips and
  wafer parts".
- IMAPS 2012 (Lewis et al.): selective Ni/Pd plating on single Al-cap bare die
  so wire-bond die can be solder flip chipped; also plating over Au/Cu stud bumps.
  <https://imapsource.org/article/66866-processing-bumping-and-assembly-of-single-chip-plated-ni-pd-over-alcap-bond-pads-for-flip-chip-applications-and-prototyping>

## 3. Stud bumping (first pass)

- Au stud bumps are made with a modified wire bonder and work on single die.
  <https://microwavejournal.com/articles/3622-gold-stud-bumps-in-flip-chip-applications>
- Sandia work: Au studs directly on Al pads are unreliable once heated to about
  200 C and above (Au-Al intermetallics); they plated electroless Ni/Au first.
  <https://www.osti.gov/servlets/purl/1109262>

## 4. Laser solder jetting (first pass)

- PacTech SB2: preformed ball placed and laser reflowed in one step, fluxless.
  SB2-Jet is pitched at single die, MEMS, probe cards. Ball sizes 60 to 760 um.
- DESY 2012 slides: solder baller is a flexible single chip bumping route and
  can use Au studs as the UBM; 60 um SAC balls used for Belle-II prototypes.
  <https://indico.desy.de/event/5679/contributions/75884/attachments/50318/61474/BumpBonding.pdf>
- PacTech also sells electroless Ni/Au, Ni/Pd, Ni/Pd/Au UBM as a contract
  service; single die acceptance needs to be confirmed with them. **(unverified)**
- CIL (UK OSAT) brought an SB2-Jet online in 2026.

## 5. Second pass (same day)

Written up in `docs/` (Sphinx, one page per method). Extra findings that fed it:

- Target geometry comes from two pin-planning spreadsheets: full area arrays,
  "250um ball", pitches mostly 0.40 to 0.65 mm, 16 to 110 balls. A note in the
  sheet says "Micross could be a good option".
- wafer.space: 5 metal layers, slots 3.93 x 5.12 mm down to 1.94 x 2.53 mm,
  1000 dies per slot, custom or no pad ring allowed, chip-on-board add-on
  $1,500, full undiced 200 mm wafer listed at $2,000 (text looked stale).
- gf180mcuD top metal is 11 kA (1.1 um); gf180mcuC is 9 kA. GF reported pad
  delamination with the thinner one.
- GF180MCU design manual section 9.4.3 has solder bump pad rules (TM.1 to
  TM.10). A 200 um opening gives a minimum pitch of 356 um.
- Virginia Tech thesis (Jittinorasett, 1999) read in full for the single-die
  ENIG recipe: 50% nitric 5 s, zincate 30 s twice, Ni 88 C pH 5 for 15 min
  (5 um), Au 90 C 1 min; double zincate removes 0.3 to 0.4 um of Al.
- Single-die stud bump services: QP Technologies (Quik-Pak), ALTER Technology,
  Hybrid SA, CMC via QP and 3IT.Micro. Laser jetting: PacTech, CIL (UK).
- CERN-hosted seminar deck (Kreidl, 2017): manual single-chip ENIG is "time
  consuming, bad yield"; "solder jetting works well".
- Found nothing showing ultrasonic, active solder or Sn-Zn working on ~1 um
  thin-film IC pads. Closest is solar cell rear-contact tinning.
- No vendor publishes prices. All cost figures in the docs are rough guesses.

Still to do: read more sources in full, get quotes, confirm wafer.space stack.

## 6. Scope change and third pass (same day)

Scope: home methods only, high failure rates fine, only needs
to work 0 to 50 C, include novel ideas, flex PCBs and Z-axis tape. Docs were
reorganised: home methods first, industry routes moved to `docs/industry/`.

- Caswell: zincate concentrate plus One-Plate 1 electroless nickel mini kit
  ($148 listed) plates aluminium if zincated first. Zincate 75 F, 15 s to
  2 min. Nickel 185 to 195 F, 15 to 60 min.
- Superior Flux "Direct Aluminum Soldering Paste" (Sn96.5Ag3.5, hot plate,
  water-soluble residue, Ag-Al intermetallic, 882 psi Al-Al lap joints). Read
  from the PDFs. Bulk aluminium only; nothing on thin film.
- Tollens / silver mirror: non-selective, alkaline, explosive silver nitride
  on standing. Thin silver leaches into molten tin.
- Brevnov et al.: silver displaces onto Al films alloyed with ~0.5% Cu but
  not onto pure Al. Selective, so worth an experiment.
- 3M 9703 Z-axis tape: minimum gap 0.4 mm, minimum pad area 3.2 mm2. Far too
  coarse for 200 um pads. Real ACF needs ~140 to 200 C and 20 bar or more.
- JLCPCB flex: 3/3 mil, ENIG, 25 or 50 um polyimide. Stencils from $7.
- Reballing: 0.25 mm balls and universal stencils (0.25 mm ball / 0.5 mm
  pitch) are cheap hobby items; MHP30 mini hot plate 30 x 30 mm.
- Gallium destroys aluminium (grain boundary attack): ruled out.
- Patents: nanosilver paste sinters onto Al pads at ~250 C without pressure.

Not yet researched: consumer aluminium fluxes, where to buy ACF in small
quantities, hobby ultrasonic irons, whether GF180MCU top metal is AlCu.

## 7. Gap filling (same day)

- Aluminium flux in small bottles: Superior No. 1260 5 oz at SRA ($38.99, old
  listing), Kapp Golden Flux 2 oz ($39), generic 10 ml bottles about $10.
- ACF reels for screen repair: about $30 for 25 to 50 m, widths 1.2 to 2.0 mm,
  short shelf life. Particle size not stated by sellers. Pulse-heat bonding
  machines from about $700.
- Ultrasonic soldering irons: listings start around $2,000. Not a hobby tool.
- Top metal alloy: not found. klayout-pex PR gives Metal5 = 40 mohm/sq on the
  11 kA stack, about 4.4 uohm cm, which hints at alloy or barrier layers.
  Whether a TiN cap remains on pads is unknown and matters a lot. Ask
  wafer.space.

## 8. Past wafer.space runs (same day)

- All packaging so far is chip-on-board wire bonding. Run 1 results: TQVA
  80/80, JKU1 20/20, GD02 19/20 boards pass. 11 designs have results.
- Run 2: 24 of 40 designs chose chip-on-board; first bare dies shipped
  2026-10-30; no bonding results yet.
- Run 2 design FC01 "Flip Chip pad test version 1": quarter slot, 12 pads, no
  transistors, no public repo. From the render: six ~220 um square pads at
  0.4 mm pitch (2 x 3) plus six ~120 x 60 um pads, joined by traces.
- Crowd Supply pages return 403 to automated fetches.

## 9. sky130 comparison and existing project documents (same day)

- google/skywater-pdk-sky130-raw-data: device measurements (MDM files) and a
  probe pad function spreadsheet for the SkyWater test tile, 12 pads per
  module. No pad size, pitch, metal or opening anywhere in it.
- skywater-pdk rules: met5 min width/space 1.6 um, 1.2 or 2 um thick; rdl
  (copper) width/space 10 um, pad enclosure 10.75 um, 15 um to seal ring;
  polyimide/PBO assumptions reference an outside bumping house.
- open_pdks sky130/custom/scripts/bump_bond_generator (micross.tech,
  bump_bond.tcl): layers PI1, RDL, PI2, UBM. UBM radius 125 um, PI2 opening
  radius 110 um, RDL pad radius 135 um, route width 15 um, PI1 via 10 um
  inside pad cut.
- caravel and caravel-gf180mcu scripts/make_bump_bonds.tcl: 6 x 10 bumps at
  500 um. sky130 die 3588 x 5188 um, GF180 die 3880 x 5070 um. GF180 pads:
  60 um glass cuts; 21 left at 205 um, 20 right at 215 um, 11 top and 11
  bottom at 275 um.

Correction to section 9: the open test tile docs in the raw data repo
(docs/sky130-testtile-open/testinterface.png) do give pad geometry:
40 x 40 um probe pads, 60 um pitch along a row, 80 um
between rows, 6 x 3 per group, over 1400 pads on the tile.
