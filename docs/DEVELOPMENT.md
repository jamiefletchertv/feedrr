# Development Guide

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

## Installing uv

If you don't have `uv` installed:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv

# Or via homebrew (macOS)
brew install uv
```

## Quick Start

### 1. Create a virtual environment

```bash
# uv will automatically create and use a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
# Install project dependencies
make install

# Or install with dev dependencies
make dev

# Or manually with uv
uv pip install -e .
uv pip install -e ".[dev]"
```

### 3. Run feedrr

```bash
# Initialize the database (first time only)
uv run feedrr init-db

# Fetch RSS feeds
make run-fetch
# or: uv run feedrr fetch --all

# Process articles with LLM
make run-process
# or: uv run feedrr process

# Generate static site
make run-generate
# or: uv run feedrr generate

# Or run the full pipeline
make run-build
# or: uv run feedrr build
```

## Development Workflow

### Running Tests

```bash
make test
# or: uv run pytest
```

### Code Formatting

```bash
# Format code with black
make format

# Check linting
make lint
```

### Clean Up

```bash
make clean
```

## Project Structure

```
feedrr/
├── .claude/              # Project documentation for LLM context
├── src/                  # Source code
│   ├── fetcher/         # RSS feed fetching
│   ├── processor/       # LLM processing
│   ├── storage/         # Database operations
│   └── generator/       # Static site generation
├── templates/           # Jinja2 templates
├── static/              # CSS/JS assets
├── data/                # SQLite database & models
├── docs/                # Project documentation
├── site/                # Generated static site (GitHub Pages)
├── config.yaml          # App configuration
├── feeds.yaml           # RSS feed sources
└── pyproject.toml       # Project dependencies
```

## Configuration

### Adding RSS Feeds

Edit `feeds.yaml`:

```yaml
sources:
  - name: "My Feed"
    feed_url: "https://example.com/rss"
    website_url: "https://example.com"
    enabled: true
    category: "tech"
```

### App Configuration

Edit `config.yaml` to customize:
- LLM model settings
- Topic taxonomy
- Fetcher behavior
- Generator output settings

## CLI Commands

Once installed, the `feedrr` command is available:

```bash
# Fetch RSS feeds
feedrr fetch [--source <name>] [--all]

# Process articles with LLM
feedrr process [--reprocess] [--limit <n>]

# Generate static site
feedrr generate [--force] [--output <dir>]

# Full pipeline
feedrr build

# Initialize database
feedrr init-db

# Show statistics
feedrr stats

# List configured sources
feedrr sources list

# Add new source
feedrr sources add <name> <feed_url>
```

## Why uv?

- **Fast**: 10-100x faster than pip
- **Reliable**: Better dependency resolution
- **Modern**: Written in Rust, actively maintained
- **Compatible**: Drop-in replacement for pip
- **All-in-one**: Handles virtual environments too

## Troubleshooting

### Virtual environment not activated

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Dependencies not installing

```bash
# Clear cache and reinstall
uv cache clean
uv pip install -e ".[dev]" --refresh
```

### Command not found: feedrr

Make sure the virtual environment is activated and the package is installed:

```bash
uv pip install -e .
```

## Next Steps

1. ✅ Set up development environment
2. Configure RSS feeds in `feeds.yaml`
3. Run initial fetch: `make run-fetch`
4. Process articles: `make run-process`
5. Generate site: `make run-generate`
6. Open `site/index.html` in browser

See `.claude/implementation-phases.md` for the full development roadmap.
