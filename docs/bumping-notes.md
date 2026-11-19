# Unverified notes on bumping aluminium pads

These notes were shared with Tim on Discord on 2026-11-10 and compiled
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
4. **Resist mould.** Thick resist, 5 to 50 µm or more, or dry film for tall
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
   - Typical thickness is 5 to 10 µm for traces and more for pads and pillars.
6. **Strip and etch.** The resist is stripped and quick wet etches remove the
   exposed seed copper and titanium. The thick plated features lose only a
   sliver.
7. **Under-bump metal.** Another polyimide layer opens over each pad, then new
   seed, resist and plating: copper, then 2 to 3 µm of nickel as a solder
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
Na₂Zn(OH)₄. Zincating means dipping aluminium into it. It is the standard
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
   aluminium is more reactive than zinc: 2 Al + 3 Zn²⁺ gives 2 Al³⁺ + 3 Zn.
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
6. Electroless nickel, about 2 to 5 µm. It grows only on the zinc-covered
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
| Zinc film is tens of nanometres | The sourced figure for aluminium consumed is 0.3 to 0.4 µm of the 1.1 µm pad, which is the larger worry ([zincate and nickel](methods/zincate-nickel.md)) |
| Nickel 2 to 5 µm | The sourced lab recipe gives 5 µm in 15 minutes ([lab recipe](industry/enig.md)) |
| Immersion gold cap | Left out of the home method. Solder the same day instead |
| Double zincate matters on small pads | Listed as optional in the home method. With 200 µm pads it is less critical, but each dip costs pad metal, so it is a trade to test |
| Route A needs repassivation because pads are under nitride | The passivation material on wafer.space die is still not published |

<!-- links: generated by update_links.py, edit _links.md instead -->
[reball-video-1]: https://www.youtube.com/watch?v=MG_TanKc0E0 "Video: BGA reballing"
[reball-video-2]: https://www.youtube.com/watch?v=7kQ6FeKp754 "Video: Spirit Electronics reball process overview"
[dataifeng]: https://www.dataifeng.com/?products/dfg-944922.html "Dataifeng DTF330 BGA rework station"
