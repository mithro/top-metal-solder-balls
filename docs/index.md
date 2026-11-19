# Solder balls on wafer.space top metal

Research into packaging methods that apply material directly to the aluminium
top metal of [wafer.space](https://wafer.space) GF180MCU chips, so that a bare
die can carry solder balls and be reflowed onto a board like a wafer-level chip
scale package.

The scope is methods simple enough to do at home, where a high failure rate is
acceptable and the parts only need to work between 0 °C and 50 °C.

```{warning}
This is a literature survey drafted by an AI model. Nothing here has been
tried on real die. Claims without a source are marked "unsourced".
```

```{figure} /_static/diagrams/home-nickel-cross-section.svg
:alt: Cross-section of a solder ball on an aluminium pad plated with nickel
:width: 100%

The first-ranked home method: zincate and a hobby electroless nickel kit, then
a 0.25 mm solder ball from a reballing stencil.
```

## Who this is for

Someone with wafer.space die, or a tapeout coming, who wants to try bumping
them on a bench at home and needs to know which method to try first, what to
buy, and how to lay out the pads.

## Where to start

- [Summary](summary.md) gives the ranking of home methods in one page.
- [Starting point](background.md) has the die, the pad rules and the target
  ball geometry.
- [Home methods](methods/index.md) has one page per method, and
  [Comparison](comparison.md) puts them side by side.
- [Next steps](next-steps.md) lists the experiments to run and the questions
  still open.

The source for this site is the
[top-metal-solder-balls repository](https://github.com/mithro/top-metal-solder-balls) on GitHub. Raw research
notes are in its [`notes/`](https://github.com/mithro/top-metal-solder-balls/tree/main/notes) directory, and problems
with these pages can be reported as
[issues](https://github.com/mithro/top-metal-solder-balls/issues). To change a
page, read
[CONTRIBUTING.md](https://github.com/mithro/top-metal-solder-balls/blob/main/CONTRIBUTING.md)
first.

```{toctree}
:maxdepth: 2
:caption: Overview

summary
background
```

```{toctree}
:maxdepth: 2
:caption: Home methods

methods/index
comparison
```

```{toctree}
:maxdepth: 1
:caption: Experiments

next-steps
research
```

```{toctree}
:maxdepth: 1
:caption: Reference

past-runs
sky130
bumping-notes
industry/index
sources
```
