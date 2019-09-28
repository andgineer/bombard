#!/usr/bin/env bash
# Installs dev environment

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

sudo python3 -m pip install --upgrade pip setuptools wheel tqdm
python3 -m pip install --user --upgrade twine
sudo python3 -m pip install -r requirements.txt
sudo python3 -m pip install requests
echo
echo -e $RED"I am going to [re]write ~/.pypirc so I remove all passwords in it if it already exists"$NC
echo
read -p "Are you sure? [YN]" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo "Aborting..."
    echo
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

cp .pypirc ~
echo
echo -e $RED"Do not forget to enter password into ~/.pypirc"$NC
echo
