# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands
- Install dev environment: `uv sync --extra dev` (uv 0.13.4 or later). Run the commands below with `uv run`, from `.venv/bin/`, or in the activated `.venv`
- Run all tests: `pytest`
- Run a single test: `pytest tests/path/to/test_file.py::test_function_name -v`
- Format code: `ruff format`
- Lint code: `ruff check --fix`
- Type check: `mypy --exclude tests/test_package src tests`

## Code Style Guidelines
- **Formatting**: Follow Google style convention. Use ruff for formatting
- **Imports**: Use isort order (enforced by ruff)
- **Types**: Strict typing is required. All functions must have type annotations
- **Naming**: Use snake_case for variables, functions, methods; PascalCase for classes
- **Docstrings**: Google-style docstrings required for public APIs
- **Error Handling**: Use appropriate exception types; include context in error messages
- **Testing**: Write tests with pytest; maintain high coverage

Respect existing code patterns when modifying files. Run linting before committing changes.

## Dependencies

- `uv.lock` pins every dependency except the build toolchain (pinned with hashes in `scripts/build-dist/requirements.txt`), and uv only resolves releases at least 7 days old. Read "Dependencies and the cooldown" in [CONTRIBUTING.md](CONTRIBUTING.md) before you change dependencies, `[tool.uv]` or `.github/dependabot.yml`.

## Pull Requests

- Title PRs as Conventional Commits (`<type>: <description>`)—we squash-merge, so the PR title becomes the commit message that drives releases; `pr-title-lint` enforces it
- `feat:`/`fix:` are for user-facing changes only: they headline the release notes and bump the version. `perf:`/`revert:` also appear in the notes (no bump); `docs:`, `refactor:`, `chore:`, `build:`, `ci:`, `test:`, `style:` are hidden
- Body lines starting with `<type>:` are parsed as extra changelog entries—don't begin description lines with a conventional-commit prefix unless that's intended
- Never edit `CHANGELOG.md`, version numbers, or `.release-please-manifest.json`—Release Please owns them
- See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines