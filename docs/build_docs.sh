#!/usr/bin/env bash
#
# Build source and translated docs in docs/_build/html
#
sphinx-build -b html docs docs/_build/html -D language=en
#sphinx-build -b html docs docs/_build/html/ru -D language=ru