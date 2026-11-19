# docs

Source for <https://top-metal-solder-balls.readthedocs.io/>, built with Sphinx
and MyST. Read the site, not these files, unless you are changing a page.

| Path | What it holds |
| --- | --- |
| [`index.md`](index.md) | Front page and the sidebar sections |
| [`methods/`](methods/) | One page per home method |
| [`industry/`](industry/) | Reference pages for routes that need lab equipment or a service |
| [`diagrams/`](diagrams/) | The script that draws every diagram |
| [`_static/diagrams/`](_static/diagrams/) | The generated SVG files. Do not edit them |
| [`_links.md`](_links.md) | Every cited source: key, URL and description |
| [`update_links.py`](update_links.py) | Copies cited sources into each page and rebuilds `sources.md` |
| [`conf.py`](conf.py) | Sphinx configuration |

How to write and check a page is in [CONTRIBUTING.md](../CONTRIBUTING.md).
