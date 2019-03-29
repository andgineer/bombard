#!/usr/bin/env bash
# Uploads built package (see build.sh) to PyPi repo
# Do not forget to test installation locally with install_local.sh
python3 -m twine upload --verbose dist/*
