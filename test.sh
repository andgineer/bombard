#!/usr/bin/env bash
#
# Run all tests
# To filter by test name use test.sh -k <pattern or substring>
#
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color
NL=$'\n'

if [[ -z "$@" ]]; then  # if selected specific test we do not run doctests
    echo
    echo "##### Doc tests #####"
    rm -rf bombard/__pycache__
    python3 -m doctest -v bombard/attr_dict.py bombard/pretty_ns.py tests/fake_args.py tests/stdout_capture.py
    DOCTESTS=$?
else
    DOCTESTS=1000
fi
echo
echo "##### Unittest tests #####"
python3.7 -m unittest discover --start-directory tests --verbose $@

if [ $? -eq 0 ]; then
  echo
  echo -e $GREEN"unit tests are success!"$NC
else
  echo
  echo -e $RED"unit tests failed"$NC
fi

if [ $DOCTESTS -eq 1000 ]; then
    echo "No doc tests were run"
    exit
elif [ $DOCTESTS -eq 0 ]; then
  echo -e $GREEN"doc tests are success!"$NC
else
  echo -e $RED"doc tests failed"$NC
fi
