# top-metal-solder-balls

[![Documentation Status](https://readthedocs.org/projects/top-metal-solder-balls/badge/?version=latest)](https://top-metal-solder-balls.readthedocs.io/en/latest/)

Read the documentation at <https://top-metal-solder-balls.readthedocs.io/>.

Ways to put solder balls on the aluminium top metal of
[wafer.space](https://wafer.space) GF180MCU chips at home, so that a bare die
can be soldered to a board like a chip-scale package.

> [!WARNING]
> This is a literature survey drafted by an AI model. Nothing has been tried
> on real die.

## Build the site

```sh
pip install -r docs/requirements.txt
sphinx-build -W -n -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html`.

## What is where

| Path | What it holds |
| --- | --- |
| [`docs/`](docs/) | The site source. Start at [`docs/index.md`](docs/index.md) |
| [`docs/diagrams/gen.py`](docs/diagrams/gen.py) | Draws every diagram on the site |
| [`docs/_links.md`](docs/_links.md) | Every cited source |
| [`notes/`](notes/) | Raw research notes, not yet checked |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How pages are written and what to run before merging |
| [`.readthedocs.yaml`](.readthedocs.yaml) | Read the Docs build settings |
