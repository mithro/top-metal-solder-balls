# Electroless Ni / Au via zincation

**How it works.** A maskless wet sequence that plates only on exposed Al:

```{figure} /_static/diagrams/enig-cross-section.svg
:alt: ENIG under bump metal with a solder ball. Nickel grows only on the exposed aluminium, so no mask is needed.
:width: 100%

ENIG under bump metal with a solder ball. Nickel grows only on the exposed aluminium, so no mask is needed.
```

1. Clean and lightly etch the pads (alkaline cleaner, then acid).
2. Zincate: an alkaline zinc bath dissolves the oxide and deposits a thin Zn
   layer by displacement, which protects the Al from re-oxidising.
3. Strip the zinc in about 50% nitric acid and zincate again. The second
   (double) zincate gives a finer, more uniform seed and better adhesion.
4. Electroless Ni-P, about 5 um, in a hot acidic bath.
5. Immersion Au, 0.05 to 0.1 um, to keep the Ni solderable. ENEPIG adds an
   electroless Pd layer between Ni and Au.

The Virginia Tech thesis by Jittinorasett is the most useful single reference
because it is exactly this on loose die. Its recipe: 50% nitric dips of about
5 s, two 30 s room-temperature dips in a commercial zincate at pH 12,
electroless Ni at 88 C and pH 5 for 15 minutes (about 1 um per 3 minutes, giving
5 um), then immersion Au at 90 C for 1 minute. Die were held on a carrier with
thermoplastic adhesive film, which also protects the backside. It reports
success across die from 0.67 mm to 6.4 x 7.5 mm ([vt-thesis]). Uyemura describes
the same sequence for wafers and notes the second zincate cycle is used when the
Al is thicker than about 0.5 um ([uyemura]). A paper presented at an IPC
conference describes selective ENIG on individual ICs, with optional thick
autocatalytic Au ([ipc-single-ic]), and IMAPS work describes Ni/Pd plating on
single Al-capped die so that wire-bond die can be solder flip chipped
([imaps-nipd]).

**Equipment and vendors.** Beakers, hotplate with temperature control, DI
water, fume extraction, a carrier and edge protection. Chemistry from plating
suppliers (Uyemura, MacDermid Alpha, Atotech/MKS and others sell wafer-grade
systems; general-purpose zincate and electroless nickel are also sold for
plating aluminium parts, but I did not find a source showing those hobby
products working on thin-film pads). As a service, PacTech built its business on
this process and offers electroless Ni/Au, Ni/Pd and Ni/Pd/Au UBM ([pactech-ipc],
[pactech-profile]), and Fraunhofer ISIT offers electroless NiAu before ball
placement ([isit]); whether either takes loose die needs asking.

**Cost.** Low in materials. No public prices found. My rough guess is a few
hundred dollars of chemistry and labware to start in-house, dominated by gold
solution and waste handling, and a four-figure lot charge from a service.

**Die versus wafer.** Works on both. On wafers it is the standard low-cost UBM.
On loose die it is "manual, time consuming and expensive" per one patent
([us6548327]) and a CERN-hosted seminar deck is blunt about the manual version:
"passivate chip edges and apply ENIG UBM: time consuming, bad yield"
([kreidl]). A 2025 detector R&D talk likewise calls ENIG flip chip "expensive
and complex for single dies, MPW or small quantities" ([lauser]).

**Reliability.** The best understood option. Ni-P is a slow-reacting barrier
for SAC solder. Known failure modes are black pad (phosphorus-rich brittle
interface) and stress from thick Ni; one study found thicker and larger Ni(P)
UBMs lowered shear strength and thermal cycling life ([chen-nip]). Board-level
data shows ENEPIG slightly ahead of ENIG after ageing ([enepig]).

**Risks specific to these die.**
- Pad consumption: 0.3 to 0.4 um lost from 1.1 um, and over-etching can
  consume a thin pad completely ([finishing], [us6503343]).
- Stray plating: bare silicon edges, the backside and any scribe-line test
  structures can plate. Edges need coating or the plating time kept short.
- Pads that are electrically different (tied to substrate, to wells, or
  floating) can plate at different rates because zincation is electrochemical.
- Ni grows sideways as well as up, about 5 um over the passivation edge for
  5 um of Ni, which is short of the 10 um overlap the design manual recommends.

**Fit: high.** The only maskless route that gives a true barrier UBM on
loose die. Needs a test coupon run before risking good die.

```{figure} /_static/diagrams/enig-flow.svg
:alt: Process flow on loose die. Blue steps are room-temperature wet steps, orange steps are hot baths.
:width: 100%

Process flow on loose die. Blue steps are room-temperature wet steps, orange steps are hot baths.
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
