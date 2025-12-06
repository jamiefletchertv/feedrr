.PHONY: help install dev test lint format clean run-fetch run-process run-generate run-build

help:
	@echo "feedrr - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies using uv"
	@echo "  make dev           Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters (ruff)"
	@echo "  make format        Format code (black)"
	@echo "  make clean         Clean up cache and build files"
	@echo ""
	@echo "Run feedrr:"
	@echo "  make run-fetch     Fetch RSS feeds"
	@echo "  make run-process   Process articles with LLM"
	@echo "  make run-generate  Generate static site"
	@echo "  make run-build     Run full build (fetch + process + generate)"

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"

test:
	uv run pytest

lint:
	uv run ruff check src/
	uv run mypy src/

format:
	uv run black src/
	uv run ruff check --fix src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

run-fetch:
	uv run feedrr fetch --all

run-process:
	uv run feedrr process

run-generate:
	uv run feedrr generate

run-build:
	uv run feedrr build
