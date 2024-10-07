# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add bnoobot to path for autodoc extension to generate files from docstrings
sys.path.insert(0, os.path.abspath('../src/bnoobot'))

#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'bnoobot'
copyright = '2024, Ben Covert'
author = 'Ben Covert'
release = '0.4.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


autodoc_inherit_docstrings = True

# Use Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Include private members (_private_method) in documentation
napoleon_include_private_with_doc = False

# Use the type hints from function annotations
napoleon_use_ivar = True  # Use `ivar` for instance variables
napoleon_use_param = True  # Do not use `param` for parameters
napoleon_use_rtype = True  # Do not use `rtype` for return types

# Control how type aliases are displayed
napoleon_type_aliases = None

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_theme_options = {
    'sidebar_hide_name': True,
    'light_css_variables': {
        'color-brand-primary': '#2980B9',
        'color-brand-content': '#2980B9',
    },
    'dark_css_variables': {
        'color-brand-primary': '#2980B9',
        'color-brand-content': '#2980B9',
    },
}

html_static_path = ['_static']

html_context = {
    'license_url': 'https://github.com/bnoobman/bnoobot/blob/main/LICENSE',
}
