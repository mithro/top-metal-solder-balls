# Notes on bumping aluminium pads (10 November 2026)

These notes were shared with Tim on Discord on 10 November 2026 and compiled
by him into a two-language document, English and Chinese. This page carries
their content into the docs.

```{warning}
The person who shared the notes said the process descriptions came from an AI
model and should be taken "with huge grains of salt". Nothing on this page has
been checked with a process engineer. Where it overlaps with sourced material
elsewhere on this site, the sourced page is the one to trust.
```

## The core problem

Almost nothing sticks to an aluminium bond pad, because aluminium grows an
oxide layer almost immediately. Industry gets around it in one of two ways:

- **Route A:** plate a redistribution layer and under-bump metal on top.
- **Route B:** zincate the pads, then electroless nickel and gold.

This is the same split used on this site, where route A is under
[wafer-level bumping](industry/wafer-level.md) and route B is the
[lab recipe](industry/enig.md) and its [home version](methods/zincate-nickel.md).

## Route A: plated redistribution and under-bump metal

```{figure} /_static/diagrams/plated-rdl-flow.svg
:alt: Nine step flow from a finished wafer through polymer, seed, resist, plating, etch, under-bump metal, ball drop and dicing
:width: 100%

Route A as described in the notes. Unverified.
```

1. **Starting wafer.** Finished die with aluminium bond pads under a silicon
   nitride passivation layer.
2. **Repassivation.** Polyimide or PBO is spun on, patterned to open over the
   bond pads, and cured. It cushions stress and insulates the new copper from
   the chip.
3. **Seed layer.** Sputter about 100 nm of titanium for adhesion and as a
   barrier, then 200 to 500 nm of copper. It covers the whole wafer and
   carries the plating current.
4. **Resist mould.** Thick resist, 5 to 50 um or more, or dry film for tall
   features. It is exposed with a stepper or mask aligner and developed to
   leave trenches where traces and pads go. A ring at the wafer edge is kept
   clear for electrical contact.
5. **Electroplating.**
   - The wafer is clamped face down in a clamshell holder. Spring fingers
     touch the seed at the edge and a lip seal keeps electrolyte off them.
   - It is lowered into a fountain of acid copper sulfate and spun, with the
     anode below, usually behind a membrane.
   - Current enters at the edge and spreads across the seed. Copper deposits
     only where seed is exposed and grows up inside the resist trenches.
   - Additives shape the deposit: a suppressor (PEG) slows growth at the top
     of features, an accelerator (SPS) speeds it at the bottom, and a leveller
     flattens it.
   - Typical thickness is 5 to 10 um for traces and more for pads and pillars.
6. **Strip and etch.** The resist is stripped and quick wet etches remove the
   exposed seed copper and titanium. The thick plated features lose only a
   sliver.
7. **Under-bump metal.** Another polyimide layer opens over each pad, then new
   seed, resist and plating: copper, then 2 to 3 um of nickel as a solder
   barrier, sometimes with a flash of gold.
8. **Bumps.** Balls are dropped through a stencil and reflowed. The
   alternative is to plate the solder directly, as a copper pillar with a
   tin-silver cap, and reflow it into domes.
9. **Back end.** Backgrind, laser mark, dice, tape and reel.

The layer stack matches what the Caravel bump layout assumes: polymer, copper,
polymer, under-bump metal ([sky130 comparison](sky130.md)).

## Route B: zincate, then electroless nickel and gold

This is the cheaper under-bump metal. It skips the seed layer and the
lithography entirely. The pads are zincated, then nickel and gold are plated
chemically with no current. Plating only grows on exposed metal, so the
passivation openings do the patterning.

### What zincate is

An alkaline solution of zinc dissolved in sodium hydroxide, sodium zincate,
Na2Zn(OH)4. Zincating means dipping aluminium into it. It is the standard
trick for plating onto aluminium.

### The problem it solves

Aluminium grows a tough oxide within milliseconds of touching air or water.
Metal will not deposit on it, or peels off afterwards. Cleaning it away does
not help because it regrows at once, even in rinse water.

### How it works

```{figure} /_static/diagrams/zincate-mechanism-flow.svg
:alt: Five steps from dissolving the oxide to nickel replacing the zinc film
:width: 100%

The zincate mechanism as described in the notes.
```

1. The strongly alkaline bath dissolves the aluminium oxide.
2. With bare aluminium exposed, a displacement reaction happens, because
   aluminium is more reactive than zinc: 2 Al + 3 Zn(2+) gives 2 Al(3+) + 3 Zn.
3. The reaction limits itself once the surface is covered. It leaves a very
   thin zinc film, tens of nanometres, bonded straight to the aluminium with
   no oxide in between.
4. The zinc film protects the aluminium from oxidising again during the rinse.
   In the electroless nickel bath, nickel displaces the zinc and then keeps
   growing on itself.

### Double zincate

The first zinc layer is coarse and blotchy. Stripping it in nitric acid and
zincating again gives a finer, denser, more even film. This matters for small
pads: a poor zincate causes nickel nodules, skipped plating, or pads that lift
off later.

### Full flow on aluminium pads

1. Clean.
2. Light etch.
3. Zincate.
4. Strip in nitric acid.
5. Zincate again.
6. Electroless nickel, about 2 to 5 um. It grows only on the zinc-covered
   pads.
7. Immersion gold as a thin protective cap.

No seed layer, no resist and no lithography, which is why it is the low-cost
route.

## How feasible each route is at home

- **Zincating** looks somewhat feasible for someone comfortable with the
  chemistry.
- **Electroplating** is somewhat feasible but needs a fair amount of
  specialised equipment, on the level of a well-equipped home semiconductor
  lab.

## Leads to follow

- **Ask the people who make reballing machines.** The suggestion in the notes
  is to visit a company that makes this equipment and ask how they would get
  balls to stay on these test chips.
- A [reballing video][reball-video-1] found while researching reballing.
- A [BGA rework station][dataifeng] from Dataifeng, model DTF330. The notes
  are not sure it is the same company as in the video.
- A [reball process overview][reball-video-2] from Spirit Electronics, which
  appears to pick and place solder balls one at a time.

I have not watched the videos or opened the product page.

## How this compares with the rest of the site

| Point in the notes | Elsewhere on this site |
| --- | --- |
| Zincate is feasible at home, plating much less so | Same ranking in [the comparison](comparison.md) |
| Zinc film is tens of nanometres | The sourced figure for aluminium consumed is 0.3 to 0.4 um of the 1.1 um pad, which is the larger worry ([zincate and nickel](methods/zincate-nickel.md)) |
| Nickel 2 to 5 um | The sourced lab recipe gives 5 um in 15 minutes ([lab recipe](industry/enig.md)) |
| Immersion gold cap | Left out of the home method. Solder the same day instead |
| Double zincate matters on small pads | Listed as optional in the home method. With 200 um pads it is less critical, but each dip costs pad metal, so it is a trade to test |
| Route A needs repassivation because pads are under nitride | The passivation material on wafer.space die is still not published |

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
[sra-1260]: https://sra-shops.com/flux-aluminum-solder-1260-5oz
[kapp-flux]: https://www.kappalloy.com/liquid-paste-flux/flux-for-aluminum/kapp-liquid-golden-flux/
[generic-al-flux]: https://www.walmart.com/ip/Sinyiin-10ml-bottle-Liquid-Flux-for-Pure-Aluminum-Sheet-Soldering-Liquid-Flux-No-Clean/17396371621
[us-iron-price]: https://reach.dog/shop/cheersonic/products/ultrasonic-soldering-iron
[acf-reel]: https://www.aliexpress.us/item/2255800552723491.html
[acf-amazon]: https://www.amazon.com/AC-7206U-18-Screen-Original-Anisotropic-Conductive/dp/B09BBJ6967
[acf-machine]: https://www.alibaba.fr/product-detail/Silman-ST-100SW-PLC-Core-Hot_1601428207164.html
[klayout-pex]: https://github.com/iic-jku/klayout-pex/pull/229
[alcu-barrier]: https://patents.google.com/patent/US20040253807
[ws-run1]: https://wafer.space/ws-run1/
[ws-run2]: https://wafer.space/ws-run2/
[ws-run1-cob]: https://wafer.space/ws-run1-cob/
[fc01]: https://wafer.space/ws-run2/projects/FC01.html
[fc01-render]: https://wafer.space/ws-run2/renders/FC01_full.webp
[cob-pcbs]: https://github.com/wafer-space/chip-on-board-wire-bonded-pcbs
[cob-wirebonding]: https://github.com/wafer-space/chip-on-board-wire-bonded-pcbs/blob/main/run-1/wirebonding/README.md
[cob-results-repo]: https://github.com/wafer-space/ws-run1-cob
[gfmpw0]: https://wafer.space/google-gf180mcu-mpw0/
[cs-run1]: https://www.crowdsupply.com/wafer-space/gf180mcu-run-1
[cs-cob-update]: https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/chip-on-board
[sky130-raw]: https://github.com/google/skywater-pdk-sky130-raw-data
[sky130-rules]: https://skywater-pdk.readthedocs.io/en/main/rules/periphery.html
[bump-gen]: https://github.com/RTimothyEdwards/open_pdks/tree/main/sky130/custom/scripts/bump_bond_generator
[caravel-bump-sky130]: https://github.com/efabless/caravel/blob/main/scripts/make_bump_bonds.tcl
[caravel-bump-gf180]: https://github.com/efabless/caravel-gf180mcu/blob/main/scripts/make_bump_bonds.tcl
[gatearray]: https://wafer.space/gatearray-v1
[reball-video-1]: https://www.youtube.com/watch?v=MG_TanKc0E0
[reball-video-2]: https://www.youtube.com/watch?v=7kQ6FeKp754
[sky130-open-tile]: https://github.com/google/skywater-pdk-sky130-raw-data/tree/main/docs/sky130-testtile-open
[dataifeng]: https://www.dataifeng.com/?products/dfg-944922.html
