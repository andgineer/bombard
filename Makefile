#!make
VERSION := $(shell cat bombard/version.py | cut -d= -f2 | sed 's/\"//g; s/ //')
export VERSION

.HELP: version ## Show the current version
version:
	echo ${VERSION}

.HELP: ver-bug ## Bump the version for a bug
ver-bug:
	bash ./scripts/verup.sh bug

.HELP: ver-feature ## Bump the version for a feature
ver-feature:
	bash ./scripts/verup.sh feature

.HELP: ver-release ## Bump the version for a release
ver-release:
	bash ./scripts/verup.sh release

.HELP: reqs  ## Upgrade requirements including pre-commit
reqs:
	pre-commit autoupdate
	bash ./scripts/compile_requirements.sh
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

.HELP: docs  ## Build the documentation
uninstall:
	bash ./scripts/uninstall.sh

.HELP: test  ## Run the tests
test:
	bash ./scripts/test.sh

.HELP: upload ## Upload the application
upload:
	bash ./scripts/upload.sh

.HELP: run  ## Run the application
run:
	bash ./scripts/run.sh

.HELP: lint  ## Run the lint check
lint:
	bash ./scripts/lint.sh

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
