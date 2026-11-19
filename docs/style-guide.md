# Docs style guide

How pages on this site are written and checked. It has two sources: the rules
Tim has set for this project, and the feedback Tim (GitHub login `mithro`) has
given on documentation in other open source projects.

```{note}
The second group was gathered by an AI model reading public GitHub issues and
pull requests on 2026-11-19. The model could not read most inline review
comments, so the points are paraphrased, not quoted, and each one links to the
thread it came from. The evidence is mostly about docs tooling. Nothing was
found in Tim's own words about prose style or units, so those rules are
marked as house choices.
```

## Project rules

These come from Tim directly, in this project.

- **Everything ends up on Read the Docs, with proper diagrams.** Work in
  progress goes in `notes/` in the repository and is written up here.
- **Home methods only.** A method belongs in [Home methods](methods/index.md)
  only if it can be done with hobby tools. A wide process window and a high
  failure rate are fine, and parts only need to work from 0 °C to 50 °C.
  Anything that needs a wire bonder, a vacuum system or an outside service
  goes under [Industry routes](industry/index.md) as reference.
- **Say "proprietary", not "commercial".**
- **GF180MCU is the target.** All tests are planned on the gf180mcu PDK.
  sky130 material is comparison only.
- **The top metal is aluminium on the 11 kÅ stack.** The 9 kÅ option is not in
  use, so do not plan around it.

## What Tim asks for in docs elsewhere

| Rule | Where it comes from |
| --- | --- |
| Publish as a Sphinx site on Read the Docs and link it from the README. HTML is nicer to read and rebuilds on every commit. | [migen #13](https://github.com/m-labs/migen/issues/13), [synth_opt_adders #13](https://github.com/tdene/synth_opt_adders/issues/13) |
| Check the rendered site, not only the source. Missing examples and broken images are review comments. | [f4pga-v2x #78](https://github.com/chipsalliance/f4pga-v2x/pull/78), [skywater-pdk #143](https://github.com/google/skywater-pdk/pull/143) |
| Generate diagrams with a tool from the source of truth, in preference to hand-drawn pictures. | [sky130_xsection #1](https://github.com/klayoutmatthias/sky130_xsection/issues/1), [skywater-pdk #87](https://github.com/google/skywater-pdk/issues/87) |
| Diagrams sit in the page theme with a transparent background, not a white box. | [f4pga-v2x #78](https://github.com/chipsalliance/f4pga-v2x/pull/78) |
| Pages of the same kind follow the same template: description, then diagrams, then the detail. | [f4pga-v2x #50](https://github.com/chipsalliance/f4pga-v2x/issues/50) |
| Provide summary tables, generated from data where possible. | [skywater-pdk #86](https://github.com/google/skywater-pdk/issues/86) |
| The README has a clear title, a quick start and a link to the hosted docs. There is exactly one README. | [voc #233](https://github.com/beeware/voc/issues/233), [f4pga-v2x #42](https://github.com/chipsalliance/f4pga-v2x/pull/42) |
| State the licence of the docs on the docs. It may differ from the code licence. Use a `LICENSE` file and SPDX identifiers. | [sphinx_symbiflow_theme #30](https://github.com/SymbiFlow/sphinx_symbiflow_theme-old/issues/30), [f4pga/ideas #47](https://github.com/f4pga/ideas/issues/47) |
| Keep `conf.py` thin. Logic belongs in a script or an extension. | [gf180mcu-pdk #39](https://github.com/google/gf180mcu-pdk/pull/39) |
| Use one markup pipeline and make sure links between pages keep working. | [f4pga/ideas #49](https://github.com/f4pga/ideas/issues/49) |
| Keep pull requests tidy: accurate title, no stray whitespace, and follow-up work moved to issues so it does not block the merge. | [skywater-pdk #143](https://github.com/google/skywater-pdk/pull/143), [f4pga-examples #88](https://github.com/chipsalliance/f4pga-examples/pull/88) |

Tim's own recent docs repository,
[bmc-open-firmware-docs](https://github.com/mithro/bmc-open-firmware-docs),
adds conventions that this site also follows. They are inferred from that
repository, not from review comments:

- Every claim needs a source, and anything not checked on hardware is marked.
- Never guess a URL. A link that 404s is worse than no link. Where a page has
  gone, link an archived copy.
- Warnings are build errors.
- Dates are ISO 8601, `YYYY-MM-DD`.
- Say plainly that the content was drafted by an AI model.

## How this site applies them

### Claims and sources

- A claim from a source carries a citation such as `[vt-thesis]`. The keys
  and URLs live in `docs/_links.md`, one line each, with a description.
  `docs/update_links.py` copies the ones a page cites to the end of that page
  and rebuilds [Sources](sources.md).
- A claim that is the author's own inference is marked "my reasoning". "I"
  on these pages is the AI model that drafted them.
- Nothing on this site has been tried on real die yet. When that changes, mark
  the result as measured and give the date.
- Prices are marked as listed or as a guess, because listings go stale.

### Method pages

Every page under [Home methods](methods/index.md) uses these sections, in this
order. A section with nothing to say is left out, and sections that only
one method needs go between "How it works" and "Fit".

1. **Idea.** One paragraph, then the cross-section diagram.
2. **How it works.** Steps or what the sources say, with the process flow
   diagram.
3. **What to buy.** A table with item, notes and price.
4. **Known problems and unknowns.**
5. **Safety.**
6. **Fit.** A one-word rating in bold, then the reason.

### Diagrams

- Every diagram is an SVG generated by `docs/diagrams/gen.py`. Change the
  script and rerun it. Do not edit the SVG files.
- Backgrounds are transparent. Cross-sections and process flows share one
  canvas width, so their text renders at one size.
- Labels must not overlap the drawing or each other. Look at the rendered page
  to check.
- A diagram redrawn from a source says so in its caption, and says which
  numbers are estimates.

### Wording and units

These are house choices. No feedback from Tim was found on them.

- Units use their proper symbols with a space: 250 µm, 0.5 mm, 50 °C, 11 kÅ.
- Dimensions use ×, as in 3.93 × 5.12 mm.
- British spelling: aluminium, passivation, metallisation.
- Headings are sentence case and short enough to fit the sidebar.

### Before merging

```sh
python3 docs/diagrams/gen.py
python3 docs/update_links.py
sphinx-build -W -n -b html docs docs/_build/html
sphinx-build -b linkcheck docs docs/_build/linkcheck
```

The first three must be clean. The link check needs a person to read it: some
sites answer 403 to any robot, which is not a broken link. Then open the built
pages and look at them.

## Not done yet

- The repository has no `LICENSE` file and the pages state no licence. Tim
  needs to choose one.
- The link check is run by hand, not in CI.

<!-- links: generated by update_links.py, edit _links.md instead -->
[vt-thesis]: https://vtechworks.lib.vt.edu/handle/10919/34792 "Virginia Tech thesis (Jittinorasett): electroless nickel and gold under-bump metal on loose die"
