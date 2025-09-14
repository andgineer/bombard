# Repository Guidelines

## Project Structure & Modules
- Source: `bombard/` (CLI in `bombard/__main__.py` and `bombard/main.py`).
- Tests: `tests/` (pytest + unittest; doctests collected from modules).
- Examples: `bombard/examples/*.yaml` (use with `--example`/`--init`).
- Tooling: `scripts/` (test, lint, run, versioning), `Makefile` (friendly targets).
- Docs: `docs/` (MkDocs), packaging via `setup.py`, metadata in `bombard/version.py`.

## Build, Test, and Dev Commands
- `make help`: list available targets.
- `make run -- [args]`: run CLI locally (e.g., `make run -- --examples`).
- `make test`: run unit tests, doctests, then pytest; filter with `scripts/test.sh -k <substr>`.
- `make lint`: run pre-commit (Ruff lint/format, mypy types install).
- `make docs`: live-serve docs with MkDocs; `make docs-ru` for RU.
- `make reqs`: update pinned deps using `uv` and pre-commit.
- Versioning: `make ver-bug|ver-feature|ver-release` updates `bombard/version.py` and creates a git tag.

## Coding Style & Naming
- Python 3.12+. Use 4-space indents; keep lines ≤100 chars (Ruff configured via pre-commit).
- Lint/Format: Ruff (imports, quotes, complexity) and `ruff-format`; tests are linted leniently.
- Types: mypy is enabled with relaxed settings; add annotations where practical.
- Conventions: `snake_case` for functions/vars, `PascalCase` for classes, tests in `tests/test_*.py`.

## Testing Guidelines
- Write pytest-style tests under `tests/`; mirror module names when possible (e.g., `test_report.py`).
- Add docstring examples; doctests are auto-collected from `bombard/*.py` and `tests/*.py`.
- Run locally with `make test`; use `-k` to target subsets. CI enforces coverage config from `.coveragerc`.

## Commit & Pull Requests
- Commits: concise, imperative subject (e.g., "Correct latency calculation").
- Before pushing: `make lint test` must pass.
- PRs: include a clear description, linked issues, behavior/rationale, and tests. Update docs/examples when user-visible behavior changes. If releasing, use the `make ver-*` flow to tag.

## Environment & Tooling Tips
- Development environment: `source ./activate.sh` (creates `.venv` with `uv` and installs `requirements.dev.txt`).
- Executable usage after install: `bombard --help`; during dev: `python -m bombard.main [args]`.
