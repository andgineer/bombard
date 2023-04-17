#!make
VERSION := $(shell cat bombard/version.py | cut -d= -f2 | sed 's/\"//g; s/ //')
export VERSION

version:
	echo ${VERSION}

ver-bug:
	bash ./scripts/verup.sh bug

ver-feature:
	bash ./scripts/verup.sh feature

ver-release:
	bash ./scripts/verup.sh release

reqs:
	bash ./scripts/compile_requirements.sh

uninstall:
	bash ./scripts/uninstall.sh

test:
	bash ./scripts/test.sh

upload:
	bash ./scripts/upload.sh

run:
	bash ./scripts/run.sh

lint:
	bash ./scripts/lint.sh
