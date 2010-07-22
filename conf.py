
import sys, os

sys.path.insert(0, 'dependencies')

extensions = ['sphinx.ext.autosummary',
              'sphinx.ext.todo', 
              'sphinx.ext.ifconfig', 
              'sphinx.ext.intersphinx', 
              'sphinx.ext.pngmath', 
              'sphinx.ext.doctest', 
              'sphinx.ext.autodoc']

todo_include_todos=True

intersphinx_mapping = {'http://docs.python.org/dev': '_static/python-inv.txt'}


# jsmath_path = "jsMath/easy/load.js"
templates_path = ['_templates']

source_suffix = '.rst'

#source_encoding = 'utf-8'

master_doc = 'index'

project = u'bits'
copyright = u'2009, Jean Daniel Browne'
#
# The short X.Y version.
version = '0.7'
# The full version, including alpha/beta/rc tags.
release = '0.7'

#language = None

#today_fmt = '%B %d, %Y'

#unused_docs = []

exclude_trees = ['_build', 'todo']

#default_role = None

#add_module_names = True

#show_authors = False

pygments_style = 'sphinx'

#modindex_common_prefix = []

html_theme = 'sphinxdoc'

#html_theme_options = {}

html_theme_path = ['_templates']

#html_title = None

#html_short_title = None

#html_logo = None

#html_favicon = None

html_static_path = ['_static']

#html_last_updated_fmt = '%b %d, %Y'

#html_use_smartypants = True

#html_sidebars = {}

#html_additional_pages = {}

#html_use_modindex = True

html_use_index = True

#html_split_index = False

#html_show_sourcelink = True

#html_use_opensearch = ''

#html_file_suffix = ''

htmlhelp_basename = 'bits'


#latex_paper_size = 'letter'

#latex_font_size = '10pt'

latex_documents = [
  # ('bits', 'bits.tex', u'Every bit counts', u'jdb', 'manual'),
  ('concurrent', 'concurrent.tex', u'Concurrent network programming with Twisted',u'Jean Daniel Browne', 'howto', False),
  ('functional', 'functional.tex', u'A journey with Python, programming styles, multicore and Pi',u'Jean Daniel Browne', 'howto', False)
]

#latex_logo = None

#latex_use_parts = False

#latex_preamble = ''

#latex_appendices = []

#latex_use_modindex = True

