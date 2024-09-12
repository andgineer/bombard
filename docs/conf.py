import sys
import os
import bombard

project = "bombard"
copyright = "2024, Andrey Sorokin"
author = "Andrey Sorokin"

version = bombard.version()
release = bombard.__version__

master_doc = 'index'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

language = 'en'
languages = ['en', 'ru']

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

pygments_style = "sphinx"

todo_include_todos = False

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]
html_css_files = ['custom.css']

htmlhelp_basename = "bombarddoc"

sys.path.insert(0, os.path.abspath('..'))

html_context = {
    'languages': [('en', '/'), ('ru', '/ru/')],
    'current_language': language,
    'display_github': True,
    'github_user': 'your_github_username',
    'github_repo': 'bombard',
    'github_version': 'master/docs/',
}

# Additional configuration for Read the Docs
if os.environ.get('READTHEDOCS') == 'True':
    html_context['current_version'] = os.environ.get('READTHEDOCS_VERSION')
    html_context['languages'] = [
        ('en', f'/{html_context["current_version"]}/'),
        ('ru', f'/{html_context["current_version"]}/ru/'),
    ]

latex_documents = [
    (master_doc, "bombard.tex", "bombard Documentation", "Andrey Sorokin", "manual"),
]

man_pages = [(master_doc, "bombard", "bombard Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "bombard",
        "bombard Documentation",
        author,
        "bombard",
        "One line description of project.",
        "Miscellaneous",
    ),
]