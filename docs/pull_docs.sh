#!/usr/bin/env bash
#
# Download translation results from transiflex to locale/
#
tx pull --all

# local build to check
sphinx-build -b html -D language=ru_RU . _build/html/ru_RU
open _build/html/ru_RU/index.html
