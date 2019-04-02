#!/usr/bin/env bash
#
# Run all tests
# To filter by test name use test.sh -k <pattern or substring>
#
if [[ -z "$@" ]]; then  # if selected specific test we do not run doctests
    echo
    echo "##### Doc tests #####"
    rm -rf bombard/__pycache__
    python3 -m doctest -v bombard/attr_dict.py
fi
echo
echo "##### Unittest tests #####"
python3.7 -m unittest discover --start-directory bombard --verbose $@
