#!/usr/bin/env bash
# Uploads built package (see build.sh) to PyPi repo
#
# This is manual upload, normally you do not need it.
# The package will be uploaded to pypi automatically when you create new release on github.
#
rm -rf build/*
rm -rf dist/*
scripts/build.sh
python3 -m twine upload --verbose dist/*
