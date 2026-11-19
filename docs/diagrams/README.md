# docs/diagrams

[`gen.py`](gen.py) draws every diagram on the site and writes the SVG files to
[`../_static/diagrams/`](../_static/diagrams/). The diagrams are generated so
that dimensions, colours and label styles stay the same across pages and can
be changed in one place.

```sh
python3 docs/diagrams/gen.py
```

The SVG files are committed so that Read the Docs does not need to run the
script. Change the script, rerun it, and commit both.
