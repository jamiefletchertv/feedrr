# feedrr

AI-powered RSS news aggregator with smart deduplication and trending detection.

Live site: **https://jamiefletcher.dev/feedrr**

## Features

### 🤖 AI-Powered Intelligence
- **Content Deduplication** - Automatically detects duplicate articles across sources using AI embeddings (85% similarity threshold)
- **Trending Detection** - Identifies stories covered by multiple sources with visual badges
- **Smart Topic Tagging** - Auto-categorizes articles using lightweight LLM (sentence-transformers)

### 📰 RSS Aggregation
- **Multi-Source Support** - Fetch from unlimited RSS/Atom feeds
- **Image Extraction** - Pulls images from RSS media tags and HTML content
- **Timezone Handling** - Properly parses dates across all timezones

### 🎨 User Interface
- **Two View Modes** - Toggle between compact list and rich card views
- **Smart Filtering** - Filter by category and AI-detected topics
- **Multi-Source Navigation** - Expandable source list for trending articles
- **Mobile-First Design** - Responsive, iOS-inspired clean interface
- **Dark/Light Themes** - (Coming soon)

### ⚡ Performance & Deployment
- **Static Site Generation** - Pre-rendered HTML for instant loading
- **GitHub Pages Hosting** - Automated deployment and updates
- **No Backend Required** - Pure static files, no server needed
- **LocalStorage Preferences** - Remembers view mode and filters

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

- **src/config/feeds.yaml** - Configure RSS feed sources
- **src/config/config.yaml** - Application settings (LLM model, topics, etc.)

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed documentation.

## Technology Stack

- **Python 3.11+** - Modern Python with type hints
- **sentence-transformers** - Lightweight AI model for embeddings (~80MB)
- **SQLite** - Local database with full relationship support
- **Jinja2** - Template engine for static site generation
- **GitHub Actions** - Automated builds and deployments

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete technical documentation and architecture
- **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Development setup and guidelines
- **[tests/](tests/)** - Comprehensive test suite with 90+ tests

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
