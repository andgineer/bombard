#!/usr/bin/env bash
# Install locally to test before uploading to PyPi
sudo python3 -m pip install -r requirements.txt --ignore-installed
sudo python3 -m pip install dist/bombard-0.4-py3-none-any.whl --upgrade
