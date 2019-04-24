#!/usr/bin/env bash
#
# Build source and translated docs in _build/html
#
make html
sphinx-build -b html -D language=ru_RU . _build/html/ru_RU
