dmypy start -- --use-fine-grained-cache
#dmypy run --verbose -- --strict --implicit-reexport --warn-unused-ignores --cache-fine-grained .
(time pre-commit run --verbose --all-files) 2>&1
