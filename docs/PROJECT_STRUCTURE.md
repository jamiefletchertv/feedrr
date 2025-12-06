# Project Structure

## Clean Root Directory

The root directory contains only what's necessary for:
- Python packaging (`pyproject.toml`, `README.md`)
- Development tools (`Makefile`, `.python-version`)
- Git configuration (`.gitignore`)
- GitHub Actions (`.github/`)
- Documentation (`.claude/`, `docs/`)
- Runtime data (`data/`, `logs/` - gitignored)
- Output (`site/` - for GitHub Pages)
- Tests (`tests/`)

```
feedrr/
├── .github/              # GitHub Actions workflows
├── .claude/              # LLM context documentation
├── .venv/                # Virtual environment (gitignored)
├── data/                 # Runtime data: database, models (mostly gitignored)
├── docs/                 # Project documentation
├── logs/                 # Application logs (gitignored)
├── site/                 # Generated static site (GitHub Pages output)
├── src/                  # ALL application code and resources
├── tests/                # Test files
├── .gitignore            # Git ignore rules
├── .python-version       # Python 3.11
├── Makefile              # Development commands
├── pyproject.toml        # Python project configuration
└── README.md             # Project readme
```

## Source Directory (`src/`)

All application code, configuration, templates, and static assets live here:

```
src/
├── feedrr/               # Main Python package
│   ├── __init__.py
│   ├── cli.py            # Command-line interface
│   ├── config.py         # ← NEW: Path resolution utilities
│   ├── fetcher/          # RSS feed fetching
│   │   └── __init__.py
│   ├── processor/        # LLM processing
│   │   └── __init__.py
│   ├── storage/          # Database operations
│   │   └── __init__.py
│   └── generator/        # Static site generation
│       └── __init__.py
├── config/               # Configuration files
│   ├── config.yaml       # Application configuration
│   └── feeds.yaml        # RSS feed sources
├── templates/            # Jinja2 HTML templates
│   └── (to be created in Phase 4)
└── static/               # CSS/JS assets
    ├── css/
    └── js/
```

## Why This Structure?

### Benefits

1. **Clean Root**
   - Easy to navigate
   - Only essential files visible
   - Clear separation of concerns

2. **Organized Source**
   - All app resources in `src/`
   - Config files with code, not scattered
   - Templates and static assets logically grouped

3. **Deployment-Friendly**
   - `site/` in root for GitHub Pages
   - Config files bundled with package
   - Clear distinction between source and output

4. **Development-Friendly**
   - Virtual environment in root (standard)
   - Makefile easily accessible
   - Test directory clearly separated

### Path Resolution

The `src/feedrr/config.py` module provides utilities to resolve paths:

```python
from feedrr.config import (
    get_config_path,     # → src/config/config.yaml
    get_feeds_path,      # → src/config/feeds.yaml
    get_templates_dir,   # → src/templates/
    get_static_dir,      # → src/static/
    get_data_dir,        # → data/
    get_logs_dir,        # → logs/
    get_site_dir,        # → site/
)
```

This ensures all components can find resources regardless of where the app is installed.

## Data Directories

### `data/` - Runtime Data
- SQLite database (`data/feedrr.db`)
- LLM model cache (`data/models/` - gitignored)
- Database backups (`data/backups/` - gitignored)

**Committed to git:** Database file (for incremental builds)
**Gitignored:** Model cache, backups

### `logs/` - Application Logs
- Application logs (`*.log`)
- Error logs
- Fetch logs

**All files gitignored**, only `.gitkeep` tracked

### `site/` - Generated Static Site
- HTML pages
- Copied static assets
- Generated from `src/templates/` and database

**Committed to git:** For GitHub Pages deployment

## Configuration Files

### `src/config/config.yaml`
Application behavior settings:
- LLM model configuration
- Topic taxonomy
- Fetcher settings
- Generator settings
- Deployment settings

### `src/config/feeds.yaml`
RSS feed sources:
- Feed URLs
- Source metadata
- Enable/disable flags

See [CONFIGURATION.md](CONFIGURATION.md) for detailed documentation.

## Templates & Static Assets

### `src/templates/`
Jinja2 HTML templates for static site generation:
- `base.html` - Base layout
- `index.html` - Homepage
- `article.html` - Article page
- `topic.html` - Topic listing page

(To be created in Phase 4)

### `src/static/`
CSS and JavaScript assets:
- `css/` - Stylesheets
- `js/` - JavaScript files

These are copied to `site/` during generation.

## Tests

### `tests/`
- Unit tests
- Integration tests
- Test fixtures

Test results and coverage reports are gitignored.

Run tests: `make test`

## Documentation

### `docs/`
Project documentation:
- `DEVELOPMENT.md` - Development guide
- `CONFIGURATION.md` - Configuration guide
- `GITHUB_PAGES_SETUP.md` - Deployment guide
- `PROJECT_STRUCTURE.md` - This file
- `LOCAL_TEST_RESULTS.md` - Test results

### `.claude/`
LLM context documentation:
- `project-overview.md` - Project vision and requirements
- `architecture.md` - System architecture
- `implementation-phases.md` - Development phases
- `technical-specs.md` - Technical specifications

## Comparison: Before vs After

### Before (Cluttered Root)
```
feedrr/
├── config.yaml           ← Config in root
├── feeds.yaml            ← Feeds in root
├── templates/            ← Templates in root
├── static/               ← Static in root
├── src/
│   ├── fetcher/
│   ├── processor/
│   ├── storage/
│   └── generator/
├── data/
├── docs/
├── site/
├── tests/
├── logs/
├── LOCAL_TEST_RESULTS.md ← Test doc in root
├── pyproject.toml
├── Makefile
└── README.md
```
**Root items:** 15+

### After (Clean Root)
```
feedrr/
├── .github/
├── .claude/
├── data/
├── docs/
├── logs/
├── site/
├── src/                  ← Everything app-related here
│   ├── feedrr/
│   ├── config/           ← Config moved here
│   ├── templates/        ← Templates moved here
│   └── static/           ← Static moved here
├── tests/
├── .gitignore
├── .python-version
├── Makefile
├── pyproject.toml
└── README.md
```
**Root items:** 9 visible directories + 4 files

## Quick Reference

| What You Need | Where to Find It |
|---------------|------------------|
| Add RSS feed | `src/config/feeds.yaml` |
| Change app settings | `src/config/config.yaml` |
| View generated site | `site/index.html` |
| Add template | `src/templates/` |
| Add CSS/JS | `src/static/` |
| View logs | `logs/` |
| Run tests | `make test` |
| Build site | `make run-build` |
| Documentation | `docs/` |

## Migration Notes

If you have local changes in the old locations:

1. Config files moved:
   - `config.yaml` → `src/config/config.yaml`
   - `feeds.yaml` → `src/config/feeds.yaml`

2. Templates moved:
   - `templates/` → `src/templates/`

3. Static assets moved:
   - `static/` → `src/static/`

4. Use `feedrr.config` module to resolve paths programmatically

All references in documentation have been updated to reflect the new structure.
