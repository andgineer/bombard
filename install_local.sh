#!/usr/bin/env bash
# Install locally to test before uploading to PyPi
python3 -m pip install -r requirements.txt --ignore-installed

rm -rf dist/*
./build.sh

python3 -m pip install dist/$(ls dist) --upgrade
