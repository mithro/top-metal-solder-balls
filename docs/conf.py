project = "Solder balls on wafer.space top metal"
author = "top-metal-solder-balls contributors"
copyright = "2026, top-metal-solder-balls contributors"

extensions = ["myst_parser"]
myst_enable_extensions = ["colon_fence"]
myst_heading_anchors = 3

exclude_patterns = ["_build", "diagrams", "_links.md", "README.md"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = project

# "Edit on GitHub" link at the top of every page.
html_context = {
    "display_github": True,
    "github_user": "mithro",
    "github_repo": "top-metal-solder-balls",
    "github_version": "main/docs/",
}
html_css_files = ["custom.css"]
