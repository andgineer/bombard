#!/usr/bin/env bash
#
# Create po file to translate in locale/ru_RU
#

# 1st create pot in _build/gettext
make gettext
# update
# sphinx-intl update -p _build/locale

# no create po-files with sphinx-intl
sudo pip3 install sphinx-intl
sphinx-intl update -p _build/gettext -l ru_RU
