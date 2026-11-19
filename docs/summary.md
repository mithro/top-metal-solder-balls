# Summary

Status: literature survey. Nothing here has been tried on
real die yet. Where a claim is the drafting model's own reasoning and not
something a source says, it is marked "my reasoning".

## What we are after

Solder balls, or something that does the same job, on the aluminium top metal
of wafer.space GF180MCU die, using only things that can be done at home.

- Home methods only: beakers, hobby plating kits, reballing stencils, a hot
  plate or hot air. No cleanrooms, wire bonders or bumping services.
- A wide process window and a high failure rate are acceptable. A slot yields
  1000 die, so losing most of them while learning is fine.
- It only has to "kind of work" between 0 °C and 50 °C. Thermal cycling,
  humidity and multi-year life are not requirements.

Those three constraints change the ranking a lot compared with an industry
survey. Methods that industry rejects for reliability are back in play.

```{figure} /_static/diagrams/routes.svg
:alt: The home routes covered here. Step 1 is the hard part; step 2 is ordinary reballing.
:width: 100%

The home routes covered here. Step 1 is the hard part; step 2 is ordinary reballing.
```

## Ranking for home use

1. **[Zincate plus a hobby electroless nickel kit](methods/zincate-nickel.md),
   then reball.** The home version of what industry does. About $150 to $200 of
   chemicals. Gives a real nickel surface that ordinary solder wets. The risk
   is the pad: zincate eats 0.3 to 0.4 µm of a 1.1 µm pad.
2. **[Aluminium solder paste or flux straight on the pad](methods/aluminium-solder.md).**
   The fewest steps of anything here: print, heat, rinse. Proven on bulk
   aluminium, completely untested on a 1.1 µm film. Cheap enough to just try.
3. **[A flex PCB as the package, joined with Z-axis adhesive](methods/flex-ztape.md).**
   Avoids soldering to aluminium at all. The balls go on the flex's gold pads,
   which is easy. Common Z-axis tape is too coarse, so this needs real
   anisotropic film or a different adhesive trick.
4. **[Silver epoxy dots](methods/adhesives.md).** No solder and no heat. Contact
   to bare aluminium is poor and drifts, but may be good enough at 0 to 50 °C.
5. **[Silver mirror and other silver deposits](methods/silver.md).** Easy
   chemistry, but the silver coats everything, does not remove the oxide, and
   dissolves in molten solder. More useful as a surface for epoxy than for
   solder.

[Reballing](methods/reballing.md) is common to routes 1 to 3 and is the easy
part: stencils, 0.25 mm balls and hot plates are all cheap hobby items.

The [untried ideas page](research.md) lists ideas nobody seems to have tried
that could make this much simpler.

## A test die already exists

Run 2 includes FC01, a "flip chip pad test" die with six pads of roughly
220 µm at 0.4 mm pitch. See [Past wafer.space runs](past-runs.md). The Caravel chip has a published
6 × 10 ball layout at 0.5 mm pitch for this same die size, built on added
copper and under-bump metal. See [the sky130 comparison](sky130.md).

## The one design decision that matters most

wafer.space allows any pad ring, so the pads can be designed for this. Big
round pads (200 µm or more), 0.5 mm pitch to match off-the-shelf reballing
stencils, and several pads per signal where there is room make every home
method far more forgiving. See [Starting point](background.md).
