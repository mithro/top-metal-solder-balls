# top-metal-solder-balls

Research into "packaging methods" that apply materials (solder balls, bumps,
under-bump metal, adhesives) directly to the aluminium top metal of
[wafer.space](https://wafer.space) GF180MCU chips.

- `docs/` is a Sphinx site built by Read the Docs (see `.readthedocs.yaml`).
  Start at `docs/index.md`.
- `docs/diagrams/gen.py` regenerates the SVG diagrams in `docs/_static/diagrams/`.
- `notes/` holds work-in-progress research logs, committed as the work happens.

Build the docs locally:

```sh
pip install -r docs/requirements.txt
sphinx-build -W -b html docs docs/_build/html
```

Everything here is work in progress.
