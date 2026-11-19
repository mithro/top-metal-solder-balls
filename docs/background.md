# Starting point

## Constraints

- Home methods only. No cleanroom tools, wire bonders or outside services.
- A wide process window and high failure rates are acceptable.
- It only needs to work between 0 °C and 50 °C.

## The die

| Item | Value | Source |
| --- | --- | --- |
| Process | GF180MCU, 5 metal layers, MIM caps | [wafer.space] |
| PDK variant | project template uses a fork of gf180mcuD | [template] |
| Top metal | Al, 11 kÅ (1.1 µm), the gf180mcuD stack. The 9 kÅ (0.9 µm) gf180mcuC stack is not in use on wafer.space | [open_pdks], [vlsida] |
| Slot sizes | 3.93 × 5.12 mm, 1.94 × 5.12 mm, 3.93 × 2.53 mm, 1.94 × 2.53 mm | [wafer.space] |
| Seal ring | about 26 µm per side | [wafer.space] |
| Quantity | 1000 dies per slot | [wafer.space] |
| Delivery | bare die; chip-on-board option at $1,500; full undiced 200 mm wafer listed at $2,000 | [wafer.space] |
| Pad ring | default ring for wire bonding, but "any pad ring configuration, or no pad ring at all" is allowed | [wafer.space] |
| Default I/O pad opening | 60 × 60 µm in the PDK I/O library | [gf180-io] |

Not yet confirmed: the die thickness, the passivation material and thickness,
the top metal alloy, and whether the undiced wafer option is really available
(the page text for it looked stale). These are tracked as
[open questions](next-steps.md#open-questions).

OpenLane's PDK notes say GlobalFoundries reported pad delamination problems
with the thinner 9 kÅ top metal, which is why the 11 kÅ variant exists
([openlane-pdks]). The 9 kÅ stack is not in use on wafer.space, so every die
here has the thicker metal. That still matters: every wet UBM process eats some pad metal.


```{figure} /_static/diagrams/pad-bare.svg
:alt: The starting point: an aluminium pad in a passivation opening. Dimension names follow the GF180MCU bump rules.
:width: 100%

The starting point: an aluminium pad in a passivation opening. Dimension names follow the GF180MCU bump rules.
```

## What the foundry rules already say about bumps

The GF180MCU design manual has a solder bump section ([drm-9.4.3]). With `A` as
the passivation opening (units not stated on the page, evidently µm):

| Rule | Meaning | Value |
| --- | --- | --- |
| TM.1a | minimum passivation opening | 40 |
| TM.2 / TM.2a | UBM opening | A + 20, minimum 60 |
| TM.3 / TM.3a | bump pad (top metal) | A + 32, minimum 72 |
| TM.3b | bump pad larger than UBM opening | 6 per side |
| TM.4 | pad centre to die edge | 90 |
| TM.5 | minimum bump pitch | 70 + 1.3 × (UBM opening) |
| TM.7 | pad shape | at least octagonal |
| TM.8, TM.10 | top via to UBM / passivation opening edge | 2 |

The manual also recommends at least 10 µm of UBM overlap onto the passivation
and says bumps are used with nitride or polyimide final passivation
([drm-9.4.2], [drm-9.4.1]). It does not say what UBM stack is assumed.

## Target geometry from the planning spreadsheets

Tim's two planning sheets ("SKY130 WCSP Packaging Options and Pin Planning" and
"IO expander pin planning") lay out full area arrays of balls: 49 to 110 balls
on dies of 16 to 22 mm², and 16 to 42 balls on small dies, with a note of
"250um ball" and pitches mostly between 0.40 and 0.65 mm. Applying the same
method (5% edge padding, pitch = padded size / ball count) to wafer.space slots:

| Slot | Array | Balls | Pitch X | Pitch Y |
| --- | --- | --- | --- | --- |
| 3.93 × 5.12 mm | 7 × 9 | 63 | 0.53 mm | 0.54 mm |
| 3.93 × 5.12 mm | 8 × 10 | 80 | 0.47 mm | 0.49 mm |
| 3.93 × 5.12 mm | 9 × 12 | 108 | 0.41 mm | 0.41 mm |
| 1.94 × 2.53 mm | 4 × 5 | 20 | 0.46 mm | 0.48 mm |
| 1.94 × 2.53 mm | 4 × 6 | 24 | 0.46 mm | 0.40 mm |

So the working target is **250 µm balls at 0.4 to 0.5 mm pitch**, which is
standard WLCSP territory: parts from proprietary processes use 0.40 mm pitch
with 0.25 mm balls ([nxp-wlcsp]) and Fraunhofer ISIT quotes 200 µm balls at 400 µm pitch as routine
([isit]). With a 200 µm passivation opening the GF180 rules give a 220 µm UBM
opening, a 232 µm top metal pad and a minimum pitch of 356 µm, so a 0.4 mm
array is inside the foundry's own bump rules.


```{figure} /_static/diagrams/ball-arrays.svg
:alt: Full slot with 80 and 108 balls and quarter slot with 20 balls, all 250 µm balls drawn to scale.
:width: 100%

Full slot with 80 and 108 balls and quarter slot with 20 balls, all 250 µm balls drawn to scale.
```



Two things differ from a normal WLCSP. There is no copper redistribution layer
and no polymer repassivation, so the ball sits directly over the pad on top
metal ("bump on pad"). And with full area arrays the pads sit over the core, so
circuit-under-pad rules and routing blockage on metal 5 become design questions.

## What any method has to solve

1. **Oxide.** Al carries a tough native oxide that solder flux will not remove.
   It must be chemically displaced (zincate), mechanically broken (ultrasonic,
   thermosonic stud bond) or covered under vacuum (sputter after back-etch).
2. **Barrier.** Sn must be kept away from the Al, and the wettable layer must
   survive reflow without dissolving. Ni does this well; Au and Cu alone do not.
3. **Thin pad metal.** About 1.1 µm of Al. Double zincation removes roughly
   0.3 to 0.4 µm, and 1 µm is the usually quoted minimum ([vt-thesis],
   [us6503343]).
4. **Passivation as solder mask.** The UBM should seal over the edge of the
   passivation opening so that no bare Al is exposed to flux or moisture.
5. **Handling loose die.** Most bumping tools take wafers. Die need a carrier,
   and wet processes must not plate on the exposed silicon edges and backside.
6. **Strain.** A 5 mm silicon die soldered straight to FR4 puts the expansion
   mismatch on the balls and on the pad stack. Over a 0 to 50 °C range this is
   small, and a [flex circuit](methods/flex-ztape.md) under the die absorbs it.

At home, items 1 and 3 are the ones that decide success. Items 2 and 4 are
about lifetime and can largely be ignored for a 0 to 50 °C part.

<!-- links: generated by update_links.py, edit _links.md instead -->
[wafer.space]: https://wafer.space/ "wafer.space home page: slots, pricing and delivery options"
[template]: https://github.com/wafer-space/gf180mcu-project-template "wafer.space GF180MCU project template"
[open_pdks]: https://github.com/rtimothyedwards/open_pdks "open_pdks, the open PDK installer"
[vlsida]: https://vlsida.github.io/chip-tutorials/gf180mcu.html "VLSI DA chip tutorial: GF180MCU metal stacks"
[openlane-pdks]: https://openlane2.readthedocs.io/en/latest/usage/about_pdks.html "OpenLane 2 documentation: about PDKs"
[gf180-io]: https://gf180mcu-pdk.readthedocs.io/en/latest/IPs/IO/gf180mcu_fd_io/features.html "GF180MCU PDK documentation: I/O library features"
[drm-9.4.1]: https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_1.html "GF180MCU design manual 9.4.1"
[drm-9.4.2]: https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_2.html "GF180MCU design manual 9.4.2"
[drm-9.4.3]: https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_3.html "GF180MCU design manual 9.4.3: solder bump rules"
[nxp-wlcsp]: https://www.mouser.com/pdfdocs/AN3846.PDF "NXP application note AN3846: wafer-level chip scale packages"
[isit]: https://web.archive.org/web/20250621082454/https://www.isit.fraunhofer.de/en/technology/micro-manufacturing-processes/processes-on-wafer-level/waferbumping-balling.html "Fraunhofer ISIT: wafer bumping and balling (archived copy)"
[vt-thesis]: https://vtechworks.lib.vt.edu/handle/10919/34792 "Virginia Tech thesis (Jittinorasett): electroless nickel and gold under-bump metal on loose die"
[us6503343]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6503343 "US patent 6503343: zincation of thin aluminium pads"
