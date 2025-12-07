.PHONY: help install dev test test-cov lint format clean clean-all clean-logs clean-test run-fetch run-process run-generate run-build

help:
	@echo "feedrr - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies using uv"
	@echo "  make dev           Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make lint          Run linters (ruff)"
	@echo "  make format        Format code (black)"
	@echo "  make clean         Clean cache and build files"
	@echo "  make clean-all     Clean everything (cache, build, logs, tests)"
	@echo "  make clean-logs    Clean log files"
	@echo "  make clean-test    Clean test results and coverage"
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
	uv run pytest -v

test-cov:
	uv run pytest --cov=src/feedrr --cov-report=html --cov-report=term

lint:
	uv run ruff check src/
	uv run mypy src/

format:
	uv run black src/
	uv run ruff check --fix src/

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-logs:
	@echo "Cleaning log files..."
	rm -f logs/*.log
	rm -f logs/*.txt

clean-test:
	@echo "Cleaning test results and coverage..."
	rm -rf tests/results/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml

clean-all: clean clean-logs clean-test
	@echo "Deep clean complete!"

run-fetch:
	uv run feedrr fetch --all

run-process:
	uv run feedrr process

run-generate:
	uv run feedrr generate

run-build:
	uv run feedrr build
