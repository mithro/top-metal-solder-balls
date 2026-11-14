# Stud bumping, then solder

**How it works.** A ball bonder makes a normal thermosonic ball bond on the Al
pad and then breaks the wire off, leaving a gold (or copper) stud about 60 to
120 um across ([hybrid]). The ultrasonic scrub breaks the oxide, so no chemistry
or mask is needed. Studs can be coined flat. The stud is then either used as the
bump itself (thermocompression, or dipped in conductive adhesive) or used as a
pedestal that solder wets.

```{figure} /_static/diagrams/stud-bump-cross-section.svg
:alt: A gold stud used as the solderable surface. The two purple regions are the reliability problems.
:width: 100%

A gold stud used as the solderable surface. The two purple regions are the reliability problems.
```

**Equipment and vendors.** A manual ball bonder such as a K&S 4524 handles 18
to 75 um gold wire ([ks4524]); used units are sold by equipment brokers, prices
on request. Services that advertise single-die stud bumping: Quik-Pak / QP
Technologies ("individual die can be directly bumped without requiring under
bump metallization", [quikpak]), ALTER Technology ([alter]), Hybrid SA
([hybrid]), and CMC Microsystems routes Canadian users to QP Technologies and
3IT.Micro ([cmc]).

**Cost.** No public prices. Stud bumping is serial, so cost scales with bump
count, but 20 to 110 bumps per die is small. My rough guess is a low
four-figure setup for a service lot, or the price of a used bonder.

**Die versus wafer.** Naturally die-level. Any bonder with a die chuck works.

**Reliability.** This is the weak point for a solder-ball use.
- Au on Al forms intermetallics on heating. Sandia found joints made with
  studs directly on Al pads unreliable once processed around 200 C and above,
  and plated Ni/Au on the pads first ([sandia]). SAC reflow peaks near 245 C.
- A gold stud is "an infinite source of gold" for tin. AuSn4 embrittles the
  joint; one article describes poor yield from studs on pre-tinned pads until a
  UBM was added over the stud ([bump-buck]). Guidance for ordinary joints is to
  keep gold below about 3 wt% ([calpoly-au]).
- Copper studs avoid gold embrittlement but need more ultrasonic force, which
  risks cracking under the pad, need forming gas, are less widely offered, and
  Cu-Al intermetallic data is thin ([bump-buck], [cu-stud]).
- A stud footprint of about 80 um is small for a 250 um ball, so the ball's
  strength would rest on a narrow neck unless several studs are clustered per
  pad or the pad is otherwise sealed.

**Variants worth knowing.** PacTech's laser jetting has been used with gold
studs as the UBM for single chips (60 um SAC balls for Belle II prototypes,
[desy]); the laser reflow is milliseconds long, which limits both gold
dissolution and Au-Al growth. Low-temperature solder (Sn-Bi, about 140 C
liquidus) or In-based solder would also keep the Au-Al interface cooler.

**Fit: medium.** Fast and chemistry-free for proving electrical function.
Not a route to parts that survive repeated reflow or thermal cycling.

```{figure} /_static/diagrams/stud-bump-flow.svg
:alt: Process flow for the stud bump route.
:width: 100%

Process flow for the stud bump route.
```

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
