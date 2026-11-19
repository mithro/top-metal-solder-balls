# top-metal-solder-balls

[![Documentation Status](https://readthedocs.org/projects/top-metal-solder-balls/badge/?version=latest)](https://top-metal-solder-balls.readthedocs.io/en/latest/)

Read the documentation at <https://top-metal-solder-balls.readthedocs.io/>.

Research into "packaging methods" that apply materials (solder balls, bumps,
under-bump metal, adhesives) directly to the aluminium top metal of
[wafer.space](https://wafer.space) GF180MCU chips.

Scope: methods simple enough to do at home, where high failure rates are
acceptable and the parts only need to work between 0 °C and 50 °C.

The docs are a literature survey drafted by an AI model (Claude). Nothing in
them has been tried on real die yet.

## Quick start

```sh
pip install -r docs/requirements.txt
sphinx-build -W -n -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html`.

## Layout

- `docs/` is a Sphinx site built by Read the Docs (see `.readthedocs.yaml`).
  Start at `docs/index.md`.
- `docs/style-guide.md` says how pages are written and what to run before
  merging.
- `docs/diagrams/gen.py` regenerates the SVG diagrams in
  `docs/_static/diagrams/`. Do not edit the SVG files by hand.
- `docs/_links.md` holds the shared source links. Run `docs/update_links.py`
  after editing it.
- `notes/` holds work-in-progress research logs, committed as the work happens.
