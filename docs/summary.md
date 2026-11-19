# Summary

The home methods ranked in the order to try them, with the reason for each
rank.

## Goal

Solder balls, or something that does the same job, on the aluminium top metal
of wafer.space GF180MCU die, using only things that can be done at home. A
high failure rate is acceptable and the parts only need to work between 0 °C
and 50 °C. The [constraints](background.md#constraints) are set out in full
on the Starting point page.

These constraints change the ranking compared with an industry survey. Methods
that industry rejects for reliability are candidates here.

```{figure} /_static/diagrams/routes.svg
:alt: The home routes covered here. Step 1 is the hard part; step 2 is ordinary reballing.
:width: 100%

The home routes covered here. Step 1 is the hard part; step 2 is ordinary reballing.
```

## Ranking for home use

1. **[Zincate plus a hobby electroless nickel kit](methods/zincate-nickel.md),
   then reball.** The home version of what industry does. About \$150 to \$200 of
   chemicals. Gives a nickel surface that ordinary solder wets. The risk
   is the pad: zincate eats 0.3 to 0.4 µm of a 1.1 µm pad.
2. **[Aluminium solder paste or flux straight on the pad](methods/aluminium-solder.md).**
   The fewest steps of anything here: print, heat, rinse. Proven on bulk
   aluminium, untested on a 1.1 µm film. Cheap enough to try.
3. **[A flex PCB as the package, joined with Z-axis adhesive](methods/flex-ztape.md).**
   Avoids soldering to aluminium at all. The balls go on the flex's gold pads,
   which is easy. Common Z-axis tape is too coarse, so this needs anisotropic
   conductive film or a different adhesive.
4. **[Silver epoxy dots](methods/adhesives.md).** No solder and no heat. Contact
   to bare aluminium is poor and drifts, but may be good enough at 0 to 50 °C.
5. **[Silver mirror and other silver deposits](methods/silver.md).** Easy
   chemistry, but the silver coats everything, does not remove the oxide, and
   dissolves in molten solder. More useful as a surface for epoxy than for
   solder.

[Reballing](methods/reballing.md) is common to routes 1 to 3 and is the easy
part: stencils, 0.25 mm balls and hot plates are all cheap hobby items.

[Comparison](comparison.md) puts the methods side by side on steps, cost and
evidence. [Untried ideas](research.md) lists approaches with no published
account on thin-film IC pads that could make the job simpler.

## A test die exists

Run 2 includes [FC01](past-runs.md#fc01-a-flip-chip-pad-test-die-on-run-2), a
flip chip pad test die with ball-sized aluminium pads. The Caravel chip has a
published 6 × 10 ball layout at 0.5 mm pitch for the full-slot die size, built
on added copper and under-bump metal. See [the sky130 comparison](sky130.md).

## Design the pads for the method

wafer.space allows any pad ring, so the pads can be designed for bumping. Big
round pads (200 µm or more), 0.5 mm pitch to match off-the-shelf reballing
stencils, and several pads per signal where there is room make every home
method more forgiving. See [Starting point](background.md).
