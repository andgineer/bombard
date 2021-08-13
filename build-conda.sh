#!/usr/bin/env bash
rm -r ./dist
mkdir dist
conda-build --output-folder dist -c conda-forge .
