# Attaching solder balls to the Al top metal of wafer.space chips: method survey

Status: first-pass literature and vendor survey, 2026-11-14. Nothing here has
been tried on real die yet. Cost figures are flagged as either sourced or as a
rough guess; most vendors do not publish prices, so the guesses need quotes
behind them before anyone relies on them.

## 1. Short version

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

## 2. Starting point

### The die

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

### What the foundry rules already say about bumps

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

### Target geometry from the planning spreadsheets

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

Two things differ from a normal WLCSP. There is no copper redistribution layer
and no polymer repassivation, so the ball sits directly over the pad on top
metal ("bump on pad"). And with full area arrays the pads sit over the core, so
circuit-under-pad rules and routing blockage on metal 5 become design questions.

## 3. What any method has to solve

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
6. **Strain.** A 5 mm silicon die soldered straight to FR4 with no underfill
   puts the full expansion mismatch on the balls and on the pad stack. Corner
   balls are the usual first failures, so underfill may be needed regardless.

## 4. Methods

### 4.1 Electroless Ni / immersion Au (ENIG, ENEPIG) via zincation

**How it works.** A maskless wet sequence that plates only on exposed Al:

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

### 4.2 Stud bumping with a wire bonder, then solder

**How it works.** A ball bonder makes a normal thermosonic ball bond on the Al
pad and then breaks the wire off, leaving a gold (or copper) stud about 60 to
120 um across ([hybrid]). The ultrasonic scrub breaks the oxide, so no chemistry
or mask is needed. Studs can be coined flat. The stud is then either used as the
bump itself (thermocompression, or dipped in conductive adhesive) or used as a
pedestal that solder wets.

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

### 4.3 Sputtered or evaporated UBM

**How it works.** The industrial standard: under vacuum, sputter-etch the oxide
off the pad, then deposit an adhesion/barrier layer (Ti or TiW), a wettable
layer (Ni, NiV or Cu) and a thin Au cap (100 to 200 nm) ([ubm-interface]).
Patterning is by photolithography and etch or lift-off on wafers. For loose
die the practical options are a shadow mask aligned over the pads, or mounting
die in a carrier wafer and doing lift-off lithography.

**Equipment and vendors.** A sputter or e-beam system with in-situ etch, plus a
laser-cut shadow mask. University cleanrooms and MEMS foundries have this.
At 200 um-plus features and 0.4 mm pitch a shadow mask is realistic, which is
not true at wire-bond pad sizes.

**Cost.** Cleanroom hourly rates plus masks. My rough guess is a few hundred
to low thousands of dollars per run at an academic facility.

**Die versus wafer.** Best on wafers. On die it needs a carrier, a mask and
alignment to maybe 20 um, done by hand under a microscope.

**Reliability.** Excellent when the wettable layer is thick enough. A thin
sputtered Ni (a few hundred nm) can be consumed by SAC solder over multiple
reflows, which is why production flows plate thick Cu or Ni on top.

**Fit: medium.** Attractive if cleanroom access exists, and it avoids eating
the pad. Without in-situ oxide removal the contact resistance is unreliable.

### 4.4 Putting the ball on: laser jetting, stencil placement, paste printing

These are not alternatives to a UBM. They are the second step after 4.1 to 4.3.

**Laser solder jetting (PacTech SB2).** A preformed ball is singulated into a
capillary, melted by a laser pulse and expelled onto the pad with inert gas, so
placement and reflow happen together with no flux and no mask ([sb2-paper]).
Ball sizes run from about 60 to 760 um, and the SB2-Jet is marketed for single
die, MEMS and probe cards ([cil]). The CERN-hosted deck says "solder jetting
works well" for single chips and names PacTech ([kreidl]). CIL in the UK brought
an SB2-Jet online in 2026 and takes contract work ([cil]). The UBM must already
be wettable. Serial, so about 100 balls per die is quick. Fit: high as a
service for small lots.

**Stencil or preform ball placement.** Print or dab tacky flux, drop balls
through a stencil or a laser-drilled preform that matches the array, reflow,
clean ([isit], [reball-patent]). This is how BGA reballing works and 250 um
balls are a standard reballing size. A patent on hand-scale ball attach warns
that flux choice matters: a commercial flux gave bridging and 0% yield in its
no-stencil test ([flux-patent]). Fit: high, and it is the realistic in-house
method. Needs a small custom stencil and a die nest.

**Solder paste printing.** Print paste over the UBM and reflow into a bump, as
in Loughborough's work on electroless-Ni wafers ([lboro]). Gives lower, less
uniform bumps than preformed balls. Fit: medium.

### 4.5 Ultrasonic and active solders that wet aluminium directly

**How it works.** An ultrasonic iron or bath cavitates the molten solder, which
erodes the oxide so that solder wets Al without flux ([us-solder], [ohsu]).
Active solders (S-Bond: Sn-Ag-Ti with Ce and Ga, melting about 221 to 232 C;
Cerasolzer) add reactive elements and are spread with mechanical agitation
([sbond], [cerasolzer]).

**Evidence on thin films.** The closest work is in solar cells, where
ultrasonic tinning of evaporated or printed Al rear contacts makes real
metal-to-metal contact, with local passivation damage where the tip first
touches ([ise-us], [isfh]). Those are tens-of-micron or whole-surface layers
and millimetre-wide joints, not a 200 um pad of 1.1 um Al beside CMOS.

**Problems for this use.** Cavitation erodes the substrate itself, which is
how it works, and there is very little Al to erode. Molten tin dissolves Al.
There is no barrier layer afterwards, and the Sn-Al interface is prone to
galvanic corrosion in moisture. No vendor offers a 200 um ultrasonic tip, and
ultrasonic energy next to circuits under the pad risks cracking dielectric.

**Cost.** An ultrasonic soldering station runs from hundreds to a few
thousand dollars (rough guess), and active solder is sold in small quantities.

**Fit: low, but cheap to test.** One experiment would settle it: pre-tin large
test pads with an ultrasonic iron, then attach normal balls to the tinned pad.

### 4.6 Sn-Zn solders

Sn-Zn alloys are the traditional solder for aluminium because zinc's
electrode potential is close to Al's, which reduces galvanic attack
([snzn-patent]). They still need the oxide broken (aggressive flux or
ultrasonics), they oxidise readily, and Zn-rich phases corrode ([snzn-review]).
I found no study of Sn-Zn directly on IC pad metal. Fit: low. It is a possible
alloy choice inside the 4.5 experiment, not a method of its own.

### 4.7 Conductive adhesives

**Anisotropic film or paste (ACF/ACA).** Conductive particles trapped between
pad and substrate under pressure. It has been done on bare unbumped Al pads,
but contact resistance rose in accelerated tests because of oxide growth on the
pad ([cityu-acf]). It also needs a flat rigid substrate, a heated press, and a
raised feature on one side.

**Isotropic silver epoxy (ICA).** Stencil-printed dots on each pad, or studs
dipped in adhesive ([quikpak]). On bare Al the oxide keeps growing under the
adhesive and resistance drifts, so in practice it wants a noble surface (Au
stud or Ni/Au) first.

**Fit: low for "solder balls", medium as a fallback.** Stud bump plus
conductive adhesive is a legitimate chemistry-free, low-temperature assembly
route, but the result is not a reflow-solderable ball-grid part.

### 4.8 Indium bumps

Evaporated In with a thin Ti/Ni/Au UBM by lift-off is the standard for pixel
detector hybridisation ([psi-indium]). It is a cleanroom wafer process aimed
at 20 to 50 um pitch and cold compression bonding, not at 250 um reflow balls.
Fit: low.

### 4.9 Commercial wafer-level bumping on an undiced wafer

**How it works.** Buy the whole wafer, send it to a bumping house, get it
back bumped and diced. The house applies its own UBM (electroless Ni/Au, or
sputtered and plated) and places balls, optionally with repassivation and a
copper redistribution layer.

**Vendors.** Micross AIT (US) lists WLCSP ball place, bump-on-pad and
bump-on-polymer, Cu redistribution with polymer repassivation, wafers up to
200 mm, and explicitly "a single wafer" ([micross]); Tim's sheet already notes
Micross as a candidate. PacTech (electroless Ni/Au plus ball placement,
[pactech-ipc]). Fraunhofer ISIT (200 um balls at 400 um pitch, optional
electroless NiAu, [isit]). Fraunhofer IZM-ASSID (electroplated bumping on
200/300 mm, [izm]).

**Cost.** wafer.space lists the undiced wafer at $2,000 ([wafer.space]).
Bumping lot charges are not published; my rough guess is $5k to $20k for a
single-wafer engineering lot, more with redistribution masks.

**Reliability.** The best available, and the only route with a qualified
process behind it.

**Catches.** The wafer carries every customer's design from the run, so the
bumping layout would only match our die, and handing over a wafer of other
people's designs needs wafer.space's agreement. The die would also need to be
laid out to the bump house's rules before tapeout.

**Fit: high if the goal is a repeatable product, low for a first experiment.**

### 4.10 The baseline to compare against

Wire bonding to a small interposer or chip-on-board is what wafer.space already
sells at $1.50 per die ([wafer.space]), and the CERN-hosted deck recommends a
wire-bond interposer for prototyping bumped chips ([kreidl]). Any solder-ball
route has to beat that on size or on signal integrity to be worth the effort.

## 5. Comparison

| Method | Barrier UBM | Works on loose die | Special equipment | In-house effort | Reliability | Fit |
| --- | --- | --- | --- | --- | --- | --- |
| ENIG / ENEPIG via zincate | yes (Ni) | yes, with care | wet bench | medium | good | high |
| Au stud as UBM + solder | no | yes | ball bonder or service | low | poor to fair | medium |
| Cu stud + solder | partly | yes | Cu-capable bonder | high | unknown | low |
| Sputtered UBM via shadow mask | yes | yes, with carrier | sputter tool | high | good | medium |
| Laser jetting (ball step) | n/a | yes | service | low | good | high |
| Stencil ball placement (ball step) | n/a | yes | stencil, reflow | low | good | high |
| Ultrasonic / active solder | no | yes | ultrasonic iron | low | unknown, likely poor | low |
| Sn-Zn direct | no | yes | flux or ultrasonics | low | poor | low |
| ACF / ICA on bare Al | no | yes | press or stencil | medium | poor | low |
| Indium bumps | thin | no | cleanroom | high | n/a for reflow | low |
| Commercial wafer bumping | yes | no, needs wafer | none | low | best | high later |

## 6. Suggested next steps

1. **Design a bump test chip or test region**: octagonal top-metal pads with
   200 to 240 um openings at 0.4 and 0.5 mm pitch, daisy chains for resistance
   and continuity, a few pads tied to substrate and a few floating, and some
   60 um standard pads for comparison. Check whether the wafer.space DRC deck
   accepts large passivation openings and the UBM marker layers.
2. **ENIG trial on scrap die** from an existing run: double zincate, 5 um Ni,
   immersion Au, following the Virginia Tech sequence, with cross-sections to
   measure how much Al is left.
3. **Ball attach trial** on the plated die with a laser-cut stencil, 250 um
   SAC305 balls and tacky flux, then ball shear tests.
4. **Parallel quick look**: send a few die to a stud-bump service and to a
   laser jetting service (PacTech or CIL) for quotes and samples.
5. **Ask wafer.space** about top metal thickness, passivation stack, die
   thickness, and whether a wafer or partial wafer can be had for bumping.
6. **One cheap experiment** with an ultrasonic iron and active solder on
   scrap die, to confirm or kill the direct-to-Al idea.

## 7. Open questions

- Which GF180MCU metal stack and passivation does wafer.space actually run?
- Does the open DRC deck allow 200 um-plus passivation openings and pads over
  active circuitry in the core?
- Are scrap or reject die available for process trials?
- Is the target a hand-solderable prototype, or a part that survives
  multiple reflows and thermal cycling? That decides between 4.2 and 4.1.
- Is underfill acceptable on the target boards?
- What do single-lot quotes from Micross, PacTech, CIL and QP Technologies
  actually come to?

## 8. Sources

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

Caveats on sources: most were read as search-result summaries rather than in
full. The Virginia Tech thesis, the GF180MCU design manual pages and the
wafer.space pages were read directly. Several vendor pages are marketing
material, and the Quik-Pak release dates from 2011.
