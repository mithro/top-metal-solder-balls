# Starting point

The facts every method page relies on: what the die is, what the foundry
rules say about bumps, what ball geometry to aim for, and the problems any
method has to solve. Read this before designing pads for a tapeout.

## Constraints

- Home methods only: beakers, hobby plating kits, reballing stencils, a hot
  plate or hot air. No cleanrooms, wire bonders or bumping services.
- A wide process window and a high failure rate are acceptable. A slot yields
  1000 die, so losing most of them while learning is fine.
- It only has to "kind of work" between 0 °C and 50 °C. Thermal cycling,
  humidity and multi-year life are not requirements.

## The die

| Item | Value | Source |
| --- | --- | --- |
| Process | GF180MCU | [^wafer-space] |
| Metal layers | 5 | [^wafer-space] |
| PDK variant | a fork of gf180mcuD | [^template] |
| Top metal | aluminium | [^open_pdks][^vlsida] |
| Top metal thickness | 11 kÅ (1.1 µm) | [^open_pdks][^vlsida] |
| Seal ring | about 26 µm per side | [^wafer-space] |
| Dies per slot | 1000 | [^wafer-space] |
| Default I/O pad opening | 60 × 60 µm | [^gf180-io] |
| Pad ring | any layout, or none | [^wafer-space] |

The default pad ring is for wire bonding. wafer.space allows "any pad ring
configuration, or no pad ring at all"[^wafer-space], which is what makes large
bump pads possible.

| Slot | Width | Height |
| --- | --- | --- |
| Full | 3.93 mm | 5.12 mm |
| Half, tall | 1.94 mm | 5.12 mm |
| Half, wide | 3.93 mm | 2.53 mm |
| Quarter | 1.94 mm | 2.53 mm |

| Delivery option | Price | Source |
| --- | --- | --- |
| Bare die | included | [^wafer-space] |
| Chip-on-board | \$1,500 per slot (\$1.50 per die) | [^wafer-space] |
| Undiced 200 mm wafer | \$2,000 | [^wafer-space] |

The die thickness, the passivation and the top metal alloy are
[open questions](next-steps.md#open-questions).

The 11 kÅ stack exists because GlobalFoundries reported pad delamination with
thinner top metal[^openlane-pdks]. At 1.1 µm the pad is thin: every
wet process on this site removes some of it.

```{figure} /_static/diagrams/pad-bare.svg
:alt: The starting point: an aluminium pad in a passivation opening. Dimension names follow the GF180MCU bump rules.
:width: 100%

The starting point: an aluminium pad in a passivation opening. Dimension names follow the GF180MCU bump rules.
```

## What the foundry rules say about bumps

The GF180MCU design manual has a solder bump section[^drm-9-4-3]. `A` is the
passivation opening. The manual page does not state units; the values are
taken to be µm.

| Rule | Meaning | Value |
| --- | --- | --- |
| TM.1a | minimum passivation opening | 40 |
| TM.2 / TM.2a | UBM opening | A + 20, minimum 60 |
| TM.3 / TM.3a | bump pad (top metal) | A + 32, minimum 72 |
| TM.3b | bump pad larger than UBM opening | 6 per side |
| TM.4 | pad centre to die edge | 90 |
| TM.5 | minimum bump pitch | 70 + 1.3 × UBM opening |
| TM.7 | pad shape | at least octagonal |
| TM.8, TM.10 | top via to UBM / passivation opening edge | 2 |

The manual also recommends at least 10 µm of under-bump metal (UBM) overlap
onto the passivation and says bumps are used with nitride or polyimide final
passivation[^drm-9-4-2][^drm-9-4-1]. It does not say what UBM stack is
assumed.

## Target geometry

The target is a full area array of 250 µm balls, as on a wafer-level chip
scale package (WLCSP). Leaving 5% of each die dimension clear at the edges,
the pitch in one direction is

$$p = \frac{0.95\,L}{n}$$

where $p$ is the ball pitch in mm, $L$ is the die width or height in mm, and
$n$ is the number of balls along that side.

| Slot | Array | Balls | Pitch X | Pitch Y |
| --- | --- | --- | --- | --- |
| Full | 7 × 9 | 63 | 0.53 mm | 0.54 mm |
| Full | 8 × 10 | 80 | 0.47 mm | 0.49 mm |
| Full | 9 × 12 | 108 | 0.41 mm | 0.41 mm |
| Quarter | 4 × 5 | 20 | 0.46 mm | 0.48 mm |
| Quarter | 4 × 6 | 24 | 0.46 mm | 0.40 mm |

The working target is **250 µm balls at 0.4 to 0.5 mm pitch**, which is
standard for wafer-level chip scale packages (WLCSP): parts from proprietary
processes use 0.40 mm pitch with 0.25 mm balls[^nxp-wlcsp] and Fraunhofer
ISIT quotes 200 µm balls at 400 µm pitch as routine[^isit].

A 0.4 mm array is inside the foundry bump rules. Rule TM.5 sets the minimum
pitch as

$$p_{\min} = 70 + 1.3\,U$$

where $p_{\min}$ is the minimum bump pitch in µm and $U$ is the UBM opening
in µm, which rule TM.2 sets to the passivation opening plus 20 µm. A 200 µm
passivation opening gives $U$ = 220 µm, a 232 µm top metal pad (rule TM.3) and
$p_{\min}$ = 356 µm.

```{figure} /_static/diagrams/ball-arrays.svg
:alt: Full slot with 80 and 108 balls and quarter slot with 20 balls, all 250 µm balls drawn to scale.
:width: 100%

Full slot with 80 and 108 balls and quarter slot with 20 balls, all 250 µm balls drawn to scale.
```

Two things differ from a normal WLCSP:

- There is no copper redistribution layer and no polymer repassivation, so the
  ball sits directly over the pad on top metal ("bump on pad").
- With full area arrays the pads sit over the core, so circuit-under-pad rules
  and routing blockage on metal 5 become design questions.

## What any method has to solve

1. **Oxide.** Al carries a tough native oxide that solder flux will not remove.
   It must be chemically displaced ([zincate](methods/zincate-nickel.md)),
   attacked by a special flux ([aluminium solder](methods/aluminium-solder.md)),
   mechanically broken (ultrasonic iron, or a
   [stud bond](industry/stud-bump.md)) or removed under vacuum
   ([sputtering](industry/sputtered-ubm.md)).
2. **Barrier.** Sn must be kept away from the Al, and the wettable layer must
   survive reflow without dissolving. Ni does this well; Au and Cu alone do not.
3. **Thin pad metal.** About 1.1 µm of Al. Double zincation removes roughly
   0.3 to 0.4 µm, and 1 µm is the usually quoted minimum[^vt-thesis][^us6503343].
4. **Passivation as solder mask.** The UBM should seal over the edge of the
   passivation opening so that no bare Al is exposed to flux or moisture.
5. **Handling loose die.** Most bumping tools take wafers. Die need a carrier,
   and wet processes must not plate on the exposed silicon edges and backside.
6. **Strain.** A 5 mm silicon die soldered straight to FR4 puts the expansion
   mismatch on the balls and on the pad stack. Over a 0 to 50 °C range the
   mismatch is small, and a [flex circuit](methods/flex-ztape.md) under the die
   absorbs it.

At home, items 1 and 3 decide success. Items 2 and 4 are about lifetime and
can largely be ignored for a 0 to 50 °C part.

<!-- links: generated by update_links.py, edit _links.md instead -->
[^wafer-space]: [wafer.space home page: slots, pricing and delivery options](https://wafer.space/)
[^template]: [wafer.space GF180MCU project template](https://github.com/wafer-space/gf180mcu-project-template)
[^open_pdks]: [open_pdks, the open PDK installer](https://github.com/rtimothyedwards/open_pdks)
[^vlsida]: [VLSI DA chip tutorial: GF180MCU metal stacks](https://vlsida.github.io/chip-tutorials/gf180mcu.html)
[^gf180-io]: [GF180MCU PDK documentation: I/O library features](https://gf180mcu-pdk.readthedocs.io/en/latest/IPs/IO/gf180mcu_fd_io/features.html)
[^openlane-pdks]: [OpenLane 2 documentation: about PDKs](https://openlane2.readthedocs.io/en/latest/usage/about_pdks.html)
[^drm-9-4-3]: [GF180MCU design manual 9.4.3: solder bump rules](https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_3.html)
[^drm-9-4-2]: [GF180MCU design manual 9.4.2](https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_2.html)
[^drm-9-4-1]: [GF180MCU design manual 9.4.1](https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_1.html)
[^nxp-wlcsp]: [NXP application note AN3846: wafer-level chip scale packages](https://www.mouser.com/pdfdocs/AN3846.PDF)
[^isit]: [Fraunhofer ISIT: wafer bumping and balling (archived copy)](https://web.archive.org/web/20250621082454/https://www.isit.fraunhofer.de/en/technology/micro-manufacturing-processes/processes-on-wafer-level/waferbumping-balling.html)
[^vt-thesis]: [Virginia Tech thesis (Jittinorasett): electroless nickel and gold under-bump metal on loose die](https://vtechworks.lib.vt.edu/handle/10919/34792)
[^us6503343]: [US patent 6503343: zincation of thin aluminium pads](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6503343)
