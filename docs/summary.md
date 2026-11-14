# Summary

Status: first-pass literature and vendor survey, 2026-11-14. Nothing here has
been tried on real die yet. Cost figures are flagged as either sourced or as a
rough guess; most vendors do not publish prices, so the guesses need quotes
behind them before anyone relies on them.


```{figure} /_static/diagrams/routes.svg
:alt: Every workable route has two steps. The choice of under bump metal matters far more than how the ball is added.
:width: 100%

Every workable route has two steps. The choice of under bump metal matters far more than how the ball is added.
```

- Solder does not wet aluminium, and tin and aluminium form no useful joint, so
  every mainstream route puts a solderable, diffusion-blocking "under bump
  metal" (UBM) on the pad first and attaches the ball to that. The real question
  is how to get a UBM onto loose diced die cheaply.
- **Best fit for small batches of diced die: electroless Ni / immersion Au
  (ENIG) via double zincation, then solder balls placed by stencil or by laser
  jetting.** It is maskless, needs only beakers and a hotplate, has been shown on
  single die, and gives a real Ni barrier. The main risks are the thin top metal
  (1.1 um on the 11 kA stack, right at the commonly quoted 1 um minimum) and
  stray plating on die edges and backside.
- **Lowest effort to try first: gold stud bumps as the UBM**, done by a service
  on single die with no chemistry, followed by solder. It is quick, but Au on Al
  degrades above roughly 200 C and a gold stud is a large gold source for tin, so
  it is a prototype route, not a reliable one, unless the stud is capped.
- **Most robust: buy the undiced wafer and have it bumped commercially**
  (wafer.space lists a full undiced 200 mm wafer as an add-on). This turns the
  job into ordinary wafer-level bumping at Micross, PacTech, Fraunhofer ISIT and
  similar, at the cost of an NRE-sized lot charge and the fact that the wafer
  carries everyone's designs.
- Direct-to-aluminium tricks (ultrasonic soldering, active solders such as
  S-Bond, Sn-Zn alloys, conductive adhesives on bare Al) are real technologies
  but I found no evidence of any of them working on ~1 um thin-film pads at
  250 um ball scale. They are worth a cheap experiment, not a plan.
- Because wafer.space allows a custom pad ring or none at all, the pad geometry
  is ours to choose. Large, round or octagonal, area-array pads sized for the
  ball make every method below much easier than reusing 60 um wire-bond pads.

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
