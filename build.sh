#!/usr/bin/env bash
# Build package. For upload use upload.sh
rm -rf build/*
python3 setup.py bdist_wheel