#!/usr/bin/env bash
# Install locally to test before uploading to PyPi
sudo python3 -m pip install pyyaml>=5.1 --ignore-installed
sudo python3 -m pip install dist/bombard-0.2-py3-none-any.whl
