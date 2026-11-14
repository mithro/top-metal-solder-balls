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
