
.PHONY: check
check:
	uv run ruff check --fix
	uv run ruff format
	uv run mypy src

.PHONY: test
test:
	uv run pytest