#!/usr/bin/env bash
#
# (Re)create po file for translation in locale/ru_RU
#

# 1st create pot in _build/gettext
make gettext

# now create po-files with sphinx-intl
sudo pip3 install sphinx-intl python-levenshtein
sphinx-intl update -p _build/gettext -l ru_RU

# map transifex to po-file
TRANSIFEX_PROJECT=bombard
tx config mapping-bulk \
    --project $TRANSIFEX_PROJECT \
    --file-extension '.pot' \
    --source-file-dir _build/gettext \
    --source-lang en \
    --type PO \
    --expression 'locale/<lang>/LC_MESSAGES/{filepath}/{filename}.po' \
    --execute
