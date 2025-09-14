# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bombard is a Python load testing tool designed for stress testing HTTP servers with configurable requests. The tool allows simulation of high-load scenarios and complex request logic through YAML configuration files and optional Python inline scripting.

## Development Commands

### Testing
- `make test` or `bash ./scripts/test.sh` - Run all tests (both unittest and pytest)
- `python -m unittest --verbose` - Run unittest tests only
- `python -m pytest --verbose` - Run pytest tests only
- Filter tests with `-k <pattern>`: `bash ./scripts/test.sh -k <pattern>`

### Linting and Code Quality
- `make lint` or `bash ./scripts/lint.sh` - Run pre-commit hooks for linting
- `pre-commit run --all-files` - Run all pre-commit hooks manually
- Code uses Ruff for linting with line length of 100 characters (120 in ruff.toml)
- MyPy type checking is configured but excludes tests directory

### Documentation
- `make docs` - Build and serve English documentation locally
- `make docs-ru` - Build and serve Russian documentation locally
- Documentation is built with MkDocs and served at http://127.0.0.1:8000/

### Version Management
- `make ver-bug` - Bump version for bug fixes
- `make ver-feature` - Bump version for new features
- `make ver-release` - Bump version for releases

### Package Management
- `make reqs` - Update requirements and pre-commit hooks
- Uses `uv` for dependency management
- `requirements.in` contains direct dependencies
- `requirements.dev.txt` contains development dependencies

## Architecture

### Core Components

- **Main Entry Point**: `bombard/main.py` - CLI interface and configuration loading
- **Bombardier**: `bombard/bombardier.py` - Core load testing engine that extends WeaverMill
- **HTTP Requests**: `bombard/http_request.py` - HTTP request handling and execution
- **Configuration**: `bombard/campaign_yaml.py` - YAML configuration parsing
- **Reporting**: `bombard/report.py` - Test result reporting and statistics
- **Threading**: `bombard/weaver_mill.py` - Thread pool management for concurrent requests

### Request Execution Flow

1. Configuration loaded from YAML files (default: `bombard.yaml`)
2. Supply variables can be overridden from command line (`--supply key=value`)
3. Two main phases:
   - `prepare`: Initial setup requests (e.g., authentication)
   - `ammo`: Main load testing requests
4. Requests support variable substitution using `{variable}` syntax
5. Python scripting available inline for complex logic
6. Results aggregated and reported with statistics

### Configuration Structure

- Campaign files are YAML with `supply`, `prepare`, and `ammo` sections
- Examples available in `bombard/examples/`
- Support for request chaining, token extraction, and dynamic request generation
- Built-in variable substitution and Python eval for advanced scenarios

### Testing Structure

- Tests located in `tests/` directory
- Mixed unittest and pytest framework usage
- Test files follow `test_*.py` naming convention
- Includes functional tests, doctests, and integration tests

## Installation and Packaging

- Package distributed via PyPI as `bombard`
- Entry point: `bombard=bombard.main:main`
- Requires Python >=3.11
- Dependencies managed through `requirements.in` and compiled with `uv`

## Development Environment

- Pre-commit hooks configured for code quality
- Ruff for linting and formatting
- MyPy for type checking (excluding tests)
- Line length: 100 characters for main code, 99 for tests
- Colorama used for cross-platform terminal colors
