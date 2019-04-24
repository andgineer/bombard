#!/usr/bin/env bash
#
# map transifex to po-file
#
TRANSIFEX_PROJECT=bombard
tx config mapping-bulk \
    --project $TRANSIFEX_PROJECT \
    --file-extension '.pot' \
    --source-file-dir _build/gettext \
    --source-lang en \
    --type PO \
    --expression 'locales/<lang>/LC_MESSAGES/{filepath}/{filename}.po' \
    --execute
