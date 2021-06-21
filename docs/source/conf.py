# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "nlpretext"
author = "artefactory"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "recommonmark",
    "nbsphinx",
    "sphinx_multiversion",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "restructuredtext",
    ".md": "markdown",
}

source_parsers = {".md": "recommonmark.parser.CommonMarkParser"}

nbsphinx_execute = "never"

github_url = "https://github.com/artefactory/NLPretext"

smv_prefer_remote_refs = False
smv_remote_whitelist = None

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Autodoc parameters
always_document_param_types = True
add_module_names = False
autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"

github_url = "https://www.github.com/artefactory/nlpretext}"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # Font packages
    "fontpkg": "\\usepackage{amsmath, amsfonts, amssymb, amsthm}"
}
