# Starting point

## Constraints

- Home methods only. No cleanroom tools, wire bonders or outside services.
- A wide process window and high failure rates are acceptable.
- It only needs to work between 0 C and 50 C.

## The die

| Item | Value | Source |
| --- | --- | --- |
| Process | GF180MCU, 5 metal layers, MIM caps | [wafer.space] |
| PDK variant | project template uses a fork of gf180mcuD | [template] |
| Top metal | Al; gf180mcuD top metal is 11 kA (1.1 um), gf180mcuC is 9 kA (0.9 um) | [open_pdks], [vlsida] |
| Slot sizes | 3.93 x 5.12 mm, 1.94 x 5.12 mm, 3.93 x 2.53 mm, 1.94 x 2.53 mm | [wafer.space] |
| Seal ring | about 26 um per side | [wafer.space] |
| Quantity | 1000 dies per slot | [wafer.space] |
| Delivery | bare die; chip-on-board option at $1,500; full undiced 200 mm wafer listed at $2,000 | [wafer.space] |
| Pad ring | default ring for wire bonding, but "any pad ring configuration, or no pad ring at all" is allowed | [wafer.space] |
| Default I/O pad opening | 60 um x 60 um in the PDK I/O library | [gf180-io] |

Not yet confirmed: that wafer.space runs really are the 11 kA stack, the die
thickness, the passivation material and thickness, and whether the undiced
wafer option is really available (the page text for it looked stale).

OpenLane's PDK notes say GlobalFoundries reported pad delamination problems
with the thinner 9 kA top metal, which is why the 11 kA variant exists
([openlane-pdks]). That matters here: every wet UBM process eats some pad metal.


```{figure} /_static/diagrams/pad-bare.svg
:alt: The starting point: an aluminium pad in a passivation opening. Dimension names follow the GF180MCU bump rules.
:width: 100%

The starting point: an aluminium pad in a passivation opening. Dimension names follow the GF180MCU bump rules.
```

## What the foundry rules already say about bumps

The GF180MCU design manual has a solder bump section ([drm-9.4.3]). With `A` as
the passivation opening (units not stated on the page, evidently um):

| Rule | Meaning | Value |
| --- | --- | --- |
| TM.1a | minimum passivation opening | 40 |
| TM.2 / TM.2a | UBM opening | A + 20, minimum 60 |
| TM.3 / TM.3a | bump pad (top metal) | A + 32, minimum 72 |
| TM.3b | bump pad larger than UBM opening | 6 per side |
| TM.4 | pad centre to die edge | 90 |
| TM.5 | minimum bump pitch | 70 + 1.3 x (UBM opening) |
| TM.7 | pad shape | at least octagonal |
| TM.8, TM.10 | top via to UBM / passivation opening edge | 2 |

The manual also recommends at least 10 um of UBM overlap onto the passivation
and says bumps are used with nitride or polyimide final passivation
([drm-9.4.2], [drm-9.4.1]). It does not say what UBM stack is assumed.

## Target geometry from the planning spreadsheets

Tim's two planning sheets ("SKY130 WCSP Packaging Options and Pin Planning" and
"IO expander pin planning") lay out full area arrays of balls: 49 to 110 balls
on dies of 16 to 22 mm2, and 16 to 42 balls on small dies, with a note of
"250um ball" and pitches mostly between 0.40 and 0.65 mm. Applying the same
method (5% edge padding, pitch = padded size / ball count) to wafer.space slots:

| Slot | Array | Balls | Pitch X | Pitch Y |
| --- | --- | --- | --- | --- |
| 3.93 x 5.12 mm | 7 x 9 | 63 | 0.53 mm | 0.54 mm |
| 3.93 x 5.12 mm | 8 x 10 | 80 | 0.47 mm | 0.49 mm |
| 3.93 x 5.12 mm | 9 x 12 | 108 | 0.41 mm | 0.41 mm |
| 1.94 x 2.53 mm | 4 x 5 | 20 | 0.46 mm | 0.48 mm |
| 1.94 x 2.53 mm | 4 x 6 | 24 | 0.46 mm | 0.40 mm |

So the working target is **250 um balls at 0.4 to 0.5 mm pitch**, which is
standard WLCSP territory: commercial parts use 0.40 mm pitch with 0.25 mm balls
([nxp-wlcsp]) and Fraunhofer ISIT quotes 200 um balls at 400 um pitch as routine
([isit]). With a 200 um passivation opening the GF180 rules give a 220 um UBM
opening, a 232 um top metal pad and a minimum pitch of 356 um, so a 0.4 mm
array is inside the foundry's own bump rules.


```{figure} /_static/diagrams/ball-arrays.svg
:alt: Full slot with 80 and 108 balls and quarter slot with 20 balls, all 250 um balls drawn to scale.
:width: 100%

Full slot with 80 and 108 balls and quarter slot with 20 balls, all 250 um balls drawn to scale.
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
3. **Thin pad metal.** About 1.1 um of Al. Double zincation removes roughly
   0.3 to 0.4 um, and 1 um is the usually quoted minimum ([vt-thesis],
   [us6503343]).
4. **Passivation as solder mask.** The UBM should seal over the edge of the
   passivation opening so that no bare Al is exposed to flux or moisture.
5. **Handling loose die.** Most bumping tools take wafers. Die need a carrier,
   and wet processes must not plate on the exposed silicon edges and backside.
6. **Strain.** A 5 mm silicon die soldered straight to FR4 puts the expansion
   mismatch on the balls and on the pad stack. Over a 0 to 50 C range this is
   small, and a [flex circuit](methods/flex-ztape.md) under the die absorbs it.

At home, items 1 and 3 are the ones that decide success. Items 2 and 4 are
about lifetime and can largely be ignored for a 0 to 50 C part.

<!-- links: generated by update_links.py, edit _links.md instead -->
[wafer.space]: https://wafer.space/
[template]: https://github.com/wafer-space/gf180mcu-project-template
[open_pdks]: https://github.com/rtimothyedwards/open_pdks
[vlsida]: https://vlsida.github.io/chip-tutorials/gf180mcu.html
[openlane-pdks]: https://openlane2.readthedocs.io/en/latest/usage/about_pdks.html
[gf180-io]: https://gf180mcu-pdk.readthedocs.io/en/latest/IPs/IO/gf180mcu_fd_io/features.html
[drm-9.4.1]: https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_1.html
[drm-9.4.2]: https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_2.html
[drm-9.4.3]: https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_09_4_3.html
[nxp-wlcsp]: https://www.mouser.com/pdfdocs/AN3846.PDF
[isit]: https://www.isit.fraunhofer.de/en/technology/micro-manufacturing-processes/processes-on-wafer-level/waferbumping-balling.html
[vt-thesis]: https://vtechworks.lib.vt.edu/handle/10919/34792
[us6503343]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6503343
[us6548327]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6548327
[uyemura]: https://www.uyemura.com/under-bump-metallization-to-reduce-wafer-processing-costs.htm
[ipc-single-ic]: https://www.electronics.org/system/files/technical_resource/E8%26S33_02.pdf
[imaps-nipd]: https://imapsource.org/article/66866-processing-bumping-and-assembly-of-single-chip-plated-ni-pd-over-alcap-bond-pads-for-flip-chip-applications-and-prototyping
[pactech-ipc]: https://www.ipc.org/system/files/technical_resource/E6%26S08_01.pdf
[pactech-profile]: https://abachy.com/catalog/semiconductor-equipment/wafer-processing-equipment/thin-film-deposition-equipment/plating-equipment/pac-tech-packaging-technologies-gmbh
[kreidl]: https://indico.cern.ch/event/602046/contributions/2429701/attachments/1423997/2183622/BumpingAndFlipChipOfAsics.pdf
[lauser]: https://indico.cern.ch/event/1581713/contributions/6767522/attachments/3173934/5643703/DRD3_Week_Cern_20251114_Lauser.pdf
[chen-nip]: https://bib-pubdb1.desy.de/record/83597
[enepig]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5459027
[finishing]: https://finishing.com/08/78.shtml
[hybrid]: https://hybrid.swiss/solutions/gold-bumping/
[ks4524]: https://caeonline.com/buy/bonders/k-s-4524/9208341
[quikpak]: https://www.delphon.com/company-overview/company-news/quik-pak-offers-innovative-approach/
[alter]: https://semiconductor.altertechnology.com/flip-chip-bump-technology-au-stud/
[cmc]: https://www.cmc.ca/flip-chip-assembly-services/
[sandia]: https://www.osti.gov/servlets/purl/1109262
[bump-buck]: https://sst.semiconductor-digest.com/2008/05/choosing-the-best-bump-for-the-buck/
[calpoly-au]: https://digitalcommons.calpoly.edu/theses/605
[cu-stud]: https://sst.semiconductor-digest.com/?p=36832
[desy]: https://indico.desy.de/event/5679/contributions/75884/attachments/50318/61474/BumpBonding.pdf
[ubm-interface]: https://sst.semiconductor-digest.com/?p=36840
[sb2-paper]: https://www.researchgate.net/publication/228938323_Placement_and_reflow_of_solder_balls_for_FC_BGA_wafer-level-CSP_optoelectronic_components_and_MEMS_by_using_a_new_solder_jetting_method
[cil]: https://mail.iconnect007.com/article/149040/cil-brings-advanced-semiconductor-solder-bumping-to-the-uk/149037/smt
[reball-patent]: https://uspto.report/patent/app/20080308612
[flux-patent]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7108755
[lboro]: https://repository.lboro.ac.uk/articles/online_resource/Under_bump_metallisation_of_fine_pitch_flip-chip_using_electroless_nickel_deposition/9557078
[us-solder]: https://en.wikipedia.org/wiki/Ultrasonic_soldering
[ohsu]: https://digitalcollections.ohsu.edu/record/2584/files/3328_etd.pdf
[sbond]: https://link.springer.com/doi/10.1007/s11664-007-0190-9
[cerasolzer]: https://www.electronicdesign.com/interconnects/ultrasonic-system-bonds-unsolderable-materials
[ise-us]: https://publica.fraunhofer.de/entities/publication/e322d70d-24ca-44bf-a382-3b242f0f0cca
[isfh]: https://isfh.de/publikationen/ultrasonic-tinning-of-al-busbars-for-a-silver-free-rear-side-on-bifacial-silicon-solar-cells
[snzn-patent]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9808890
[snzn-review]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9609569
[cityu-acf]: https://scholars.cityu.edu.hk/en/publications/contact-resistance-and-adhesion-performance-of-acf-interconnectio/
[psi-indium]: https://arxiv.org/abs/physics/0510021
[micross]: https://www.micross.com/components-and-services/component-design-packaging/wafer-bumping-wlp
[izm]: https://www.izm.fraunhofer.de/content/dam/izm/en/documents/Abteilungen/High_Density_Interconnect_Wafer_Level_Packaging/Services_IZM-ASSID_Q4_15.pdf
[caswell-al]: https://support.caswellplating.com/portal/en/kb/articles/can-i-use-your-kits-to-plate-aluminum
[caswell-kit]: https://caswellplating.com/one-plate-1-electroless-nickel-kit/
[caswell-zincate]: https://caswellplating.com/zincate-8-fl-oz.html
[caswell-tutorial]: https://caswellplating.com/electroless_tutorial.html
[en-wiki]: https://en.wikipedia.org/wiki/Electroless_nickel-phosphorus_plating
[sciencemadness-en]: https://www.sciencemadness.org/whisper/viewthread.php?tid=70835
[zincate-formulas]: https://www.finishing.com/424/16.shtml
[superior-paste]: https://superiorflux.com/papers/DirectALSolderPasteIMAPS2011.pdf
[superior-guide]: https://superiorflux.com/papers/AluminumSolderingGuide.pdf
[superior-tech]: https://superiorflux.com/techniques-for-soldering-aluminum/
[tollens]: https://en.wikipedia.org/wiki/Tollens%27_reagent
[rsc-mirror]: https://edu.rsc.org/resources/a-giant-silver-mirror-experiment/822.article
[brevnov]: https://data.zhenzhi.com/details/1/908811770
[immersion-ag-patent]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6319543
[ag-mirror-al-patent]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6695458
[ag-dissolution]: https://link.springer.com/doi/10.1007/s11664-019-07316-1
[ag-leaching]: https://www.circuitnet.com/experts/87721.html
[ams2420]: https://saemobilus.sae.org/content/AMS2420E/
[stencil-kit]: https://www.amazon.com/Universal-Reballing-Stencil-Template-0-25-0-76mm/dp/B01HHQIZOC
[kit-27]: https://www.hklrf.com/27pcs-Universal-Stencil-BGA-Balls-Station-kit_1255.html
[balls-set]: https://www.amazon.com/clp/B07YXRQ4K4
[jlc-stencil]: https://jlcpcb.com/capabilities/pcb-stencil-manufacturing
[reball-guide]: https://pcbsync.com/bga-reballing-process/
[badcaps]: https://www.badcaps.net/forum/troubleshooting-hardware-devices-and-electronics-theory/equipment-usage-soldering-techniques-and-reviews/76158-noob-reballing-balling-stencil-questions
[mitxela]: https://hackaday.com/2018/06/26/no-caffeine-no-problem-a-hand-soldered-chip-scale-package/
[mhp30]: https://www.sparkfun.com/catalog/product/view/id/8333
[bisn]: https://www.caplinq.com/bi58sn42-low-eutectic-temperature-lead-free-solder-spheres-bi58sn42.html
[ica-aging]: https://incurelab.com/wp/how-conductive-epoxy-contact-resistance-changes-with-cure-and-aging
[meridian-al]: https://meridianadhesives.com/product-information-insights/tech-tip-24-bonding-to-aluminum-with-epoxy-key-challenges-and-best-practices/
[3m-9703]: https://multimedia.3m.com/mws/media/66235O/3m-electrically-conductive-adhesive-transfer-tape-9703.pdf
[3m-7303]: https://multimedia.3m.com/mws/media/66294O/3mtm-anisotropic-conductive-film-7303.PDF
[acf-params]: https://jiutustore.com/blogs/news/acf-bonding-machine-parameters-temperature-pressure-time
[jlc-flex]: https://jlcpcb.com/capabilities/flex-pcb-capabilities
[egain]: https://physicsworld.com/a/liquid-metal-disintegrates-implanted-medical-devices-on-demand/
[nanosilver-al]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8987911
[die-carrier]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6583635
[bare-die-test]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7940070
