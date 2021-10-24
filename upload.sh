#!/usr/bin/env bash
# Uploads built package (see build.sh) to PyPi repo
# Do not forget to test installation locally with install_local.sh
#
# This is manual upload.
# The package will be uploaded automatically when you create new release on github
rm -rf build/*
rm -rf dist/*
./build.sh
python3 -m twine upload --verbose dist/*
