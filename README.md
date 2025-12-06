# feedrr

RSS/News Aggregator with AI-powered topic tagging and content deduplication.

## Features

- **RSS Feed Aggregation** - Fetch and parse multiple RSS feeds
- **AI-Powered Topic Tagging** - Automatic categorization using lightweight LLM
- **Content Deduplication** - Identify duplicate articles across sources
- **Static Site Generation** - Fast, mobile-friendly web interface
- **GitHub Pages Deployment** - Automated hosting via GitHub Actions
- **Clean UI** - Mobile/Web view inspired by iOS app "feeed"

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/jamiefletchertv/feedrr.git
cd feedrr

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
make install
```

### Usage

```bash
# Initialize database
uv run feedrr init-db

# Fetch RSS feeds
make run-fetch

# Process articles with LLM
make run-process

# Generate static site
make run-generate

# Or run the full pipeline
make run-build
```

Open `site/index.html` in your browser to view the generated site.

## Configuration

- **feeds.yaml** - Configure RSS feed sources
- **config.yaml** - Application settings (LLM model, topics, etc.)

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed documentation.

## Project Scope (MVP)

Priority features:

- ✅ Multiple RSS sources
- ✅ Mobile/Web view similar to iOS app `feeed`
- ✅ Python implementation
- ✅ GitHub Pages hosting (static site generator)
- ✅ Context/topic tagging (using lightweight LLM)
- ✅ Content deduplication (using lightweight LLM)
- ⏳ Bionic reader mode (post-MVP)
- ✅ Local db/records with versioning

## Development

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for:
- Development setup
- CLI commands
- Testing and linting
- Project structure
- Contributing guidelines

## Deployment

The site is automatically deployed to GitHub Pages at:

**https://jamiefletchertv.github.io/feedrr/**

Builds run automatically:
- Every 30 minutes (scheduled)
- On every push to `main`
- Can be manually triggered

See [docs/GITHUB_PAGES_SETUP.md](docs/GITHUB_PAGES_SETUP.md) for setup instructions.

## License

MIT
