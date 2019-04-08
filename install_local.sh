#!/usr/bin/env bash
# Install locally to test before uploading to PyPi
./build.sh
sudo python3 -m pip install -r requirements.txt --ignore-installed
sudo python3 -m pip install dist/$(ls dist) --upgrade
