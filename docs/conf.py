# -*- coding: utf-8 -*-
#

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# put analyzer to the autonaysrc setting
autoanysrc_analyzers = {
    'shell-script': 'customdocs.ShellScriptAnalyzer',
    'perl-script': 'customdocs.PODAnalyzer',
}

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinxcontrib.autoanysrc',
    'sphinxcontrib.programoutput',
    'sphinxcontrib.tikz',
]

# For readthedocs
tikz_proc_suite = 'GhostScript'

# Other tikz options
tikz_latex_preamble = """
\\tikzset{
  goodstep/.style={
    minimum width=2cm,
    minimum height=1cm,
    align=center,
    draw=black,
    rounded corners=0.1cm,
    font=\\scriptsize
  },
  async/.style={
    minimum width=2cm,
    minimum height=1cm,
    align=center,
    draw=blue,
    rounded corners=0.1cm,
    font=\\scriptsize
  },
  direct/.style={
    minimum width=2.5cm,
    minimum height=0.75cm,
    align=center,
    draw=black,
    rounded corners=0.25cm
  },
  note/.style={
    minimum width=2cm,
    minimum height=1cm,
    align=center
  },
  arrow/.style={draw,thick,->,>=stealth}
}
"""

tikz_tikzlibraries = 'arrows, positioning, intersections'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Dynamo Consistency'
copyright = u'2018, Daniel Abercrombie, Max Goncharov'
author = u'Daniel Abercrombie, Max Goncharov'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u''
# The full version, including alpha/beta/rc tags.
release = u''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'DynamoConsistencydoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'DynamoConsistency.tex', u'Dynamo Consistency Documentation',
     u'Daniel Abercrombie, Max Goncharov', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'dynamoconsistency', u'Dynamo Consistency Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'DynamoConsistency', u'Dynamo Consistency Documentation',
     author, 'DynamoConsistency', 'One line description of project.',
     'Miscellaneous'),
]




# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

import mock

MOCK_MODULES = ['XRootD.client',
                'dynamo.registry.registry.RegistryDatabase',
                'dynamo.dataformat.Dataset',
                'dynamo.dataformat.Site',
                'dynamo.fileop.rlfsm.RLFSM',
                'dynamo.core.executable.inventory']

ALL_MODS = set()
for mod in MOCK_MODULES:
    while mod:
        ALL_MODS.add(mod)
        mod = '.'.join(mod.split('.')[:-1])

for mod_name in sorted(ALL_MODS):
    sys.modules[mod_name] = mock.Mock()
