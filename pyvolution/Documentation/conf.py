# -*- coding: utf-8 -*-
#
# Pyvolution documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.

# -- General configuration ----------------------------------------------------

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.intersphinx',
	'sphinx.ext.todo',
	'sphinx.ext.coverage',
	'sphinx.ext.imgmath',
	'sphinx.ext.mathjax',
	'sphinx.ext.ifconfig',
	'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Pyvolution'
copyright = '2012-2026, Ashwin Panchapakesan'

# The short X.Y version.
version = '2.0'
# The full version, including alpha/beta/rc tags.
release = '2.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages. Requires the sphinx_rtd_theme
# package (pip install sphinx_rtd_theme).
html_theme = 'sphinx_rtd_theme'

# Output file base name for HTML help builder.
htmlhelp_basename = 'Pyvolutiondoc'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
	('index', 'Pyvolution.tex', 'Pyvolution Documentation',
	 'Ashwin Panchapakesan', 'manual'),
]


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
	('index', 'pyvolution', 'Pyvolution Documentation',
	 ['Ashwin Panchapakesan'], 1)
]


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
	('index', 'Pyvolution', 'Pyvolution Documentation',
	 'Ashwin Panchapakesan', 'Pyvolution', 'Evolutionary Algorithms Framework.',
	 'Miscellaneous'),
]


# -- Options for Epub output ---------------------------------------------------

epub_title = 'Pyvolution'
epub_author = 'Ashwin Panchapakesan'
epub_publisher = 'Ashwin Panchapakesan'
epub_copyright = '2012-2026, Ashwin Panchapakesan'


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
