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

.HELP: uninstall  ## Uninstall bombard package to debug installation
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

.PHONY: docs
.HELP: docs  ## Build the English documentation
docs:
	open -a 'Google Chrome' http://127.0.0.1:8000/bombard/
	scripts/docs-render-config.sh en
	mkdocs serve -f docs/_mkdocs.yml

.HELP: docs-ru  ## Build the Russian documentation
docs-ru:
	open -a 'Google Chrome' http://127.0.0.1:8000/bombard/
	scripts/docs-render-config.sh ru
	rm -rf ./docs/src/ru/images
	cp -r ./docs/src/en/images ./docs/src/ru/images
	cp ./docs/src/en/reference.md ./docs/src/ru/reference.md
	mkdocs serve -f docs/_mkdocs.yml

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
