# feedrr - AI-Powered RSS News Aggregator

Complete documentation for the feedrr project, an RSS/News feed aggregator with AI-powered content curation.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Implementation Status](#implementation-status)
4. [Technical Specifications](#technical-specifications)
5. [Error Handling](#error-handling)

---

## Project Overview

### Vision
RSS/News Aggregator (MVP) with AI-powered features for content curation and reading enhancement.

### Core Requirements

#### Completed Features ✓
1. **RSS Feed Processing**
   - ✅ Support for multiple RSS sources
   - ✅ Reliable fetching and parsing
   - ✅ Error handling and retry logic
   - ✅ Image extraction from RSS feeds and HTML content
   - ✅ Timezone handling for date parsing

2. **Web Interface**
   - ✅ Mobile/Web view with clean, minimal layout
   - ✅ Mobile-responsive design
   - ✅ Two-view toggle (list and card view)
   - ✅ Category and topic filtering with dropdowns
   - ✅ Compact source button inline with topic tags

3. **LLM-Powered Features**
   - ✅ Topic tagging using lightweight LLM (sentence-transformers)
   - ✅ Local processing (no API costs)

4. **Static Site Hosting**
   - ✅ GitHub Pages deployment
   - ✅ Static site generation
   - ✅ Automated builds via GitHub Actions

5. **Data Management**
   - ✅ SQLite database with article records
   - ✅ Source category tracking
   - ✅ Topic associations

#### Post-MVP Features (Planned)
- [ ] Content deduplication using LLM embeddings
- [ ] Article stacking view for duplicates
- [ ] Trending topics detection
- [ ] Bionic reader mode
- [ ] Enhanced versioning and rollback capabilities
- [ ] Web scraping for article images (when RSS doesn't provide)

### Technical Decisions

#### Language & Framework
- **Python 3.11+** - Great ecosystem for LLM integration
- Modern tooling with pyproject.toml and uv package manager

#### Architecture
- **Static Site Generator** - Runs periodically via GitHub Actions
- **SQLite Database** - Local storage with version control
- **Lightweight LLM** - sentence-transformers (all-MiniLM-L6-v2, ~80MB)

#### Hosting Strategy
- **GitHub Pages** - Static site hosting at jamiefletcher.dev/feedrr
- **Pre-generation** - HTML pages generated periodically
- **Client-side enhancement** - Progressive enhancement with minimal JS

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (Scheduler)                │
│                    Runs on push to main                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RSS Feed Fetcher                          │
│  - Fetch feeds from configured sources                      │
│  - Parse RSS/Atom feeds                                      │
│  - Extract articles (title, content, date, link, image)     │
│  - Handle timezone conversions                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Processor                             │
│  - Topic Tagging (sentence-transformers)                    │
│  - Lightweight local processing                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│  - Store articles with metadata                             │
│  - Track topics and tags                                    │
│  - Source categories                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Static Site Generator                       │
│  - Jinja2 templates                                          │
│  - Generate HTML pages                                       │
│  - Category and topic filtering                             │
│  - Two view modes (list and card)                           │
│  - Output to /site folder                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Pages                             │
│  - Serve static files from /site                            │
│  - Mobile-responsive UI                                      │
│  - Fast loading (pre-generated)                              │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
feedrr/
├── .claude/              # Project documentation (legacy - merged into CLAUDE.md)
├── .github/              # GitHub Actions workflows
│   └── workflows/
│       └── deploy.yml    # Auto-deploy to GitHub Pages
│
├── src/                  # Source code
│   ├── feedrr/          # Main package
│   │   ├── cli.py       # Command-line interface
│   │   ├── fetcher/     # RSS feed fetching logic
│   │   │   └── rss.py   # Feed parsing with image extraction
│   │   ├── processor/   # LLM processing (tagging)
│   │   │   └── topics.py # Topic assignment
│   │   ├── storage/     # Database operations
│   │   │   ├── models.py # SQLAlchemy models
│   │   │   └── db.py    # Database operations
│   │   └── generator/   # Static site generation
│   │       └── site.py  # Site builder
│   ├── config/          # Configuration files
│   │   └── feeds.yaml   # RSS feed sources
│   ├── templates/       # Jinja2 HTML templates
│   │   ├── base.html    # Base layout with view toggle
│   │   └── index.html   # Article listing with filters
│   └── static/          # CSS/JS assets
│       ├── css/style.css # Styles for list and card views
│       ├── js/main.js    # View toggle and filtering
│       └── images/       # Placeholder images
│
├── data/                # SQLite database
│   └── feedrr.db
│
├── site/                # Generated static site (GitHub Pages)
│   └── (generated files)
│
├── tests/               # Test suite
│   └── test_fetcher.py  # RSS fetcher tests
│
├── pyproject.toml       # Python project configuration
├── .python-version      # Python version for uv
├── .gitignore           # Git ignore rules
├── README.md            # Project README
└── CLAUDE.md            # This file
```

### Technology Stack

#### Core Dependencies
- **feedparser** - RSS/Atom feed parsing
- **requests** - HTTP requests for fetching feeds
- **python-dateutil** - Date parsing with timezone support
- **beautifulsoup4** - HTML parsing for image extraction

#### LLM & NLP
- **sentence-transformers** - Lightweight embedding model
- **torch** - PyTorch backend for transformers

#### Database
- **SQLAlchemy** - Database ORM
- **SQLite** - Embedded database

#### Static Site Generation
- **Jinja2** - Template engine
- **PyYAML** - Configuration file parsing

#### Utilities
- **click** - CLI framework
- **rich** - Beautiful CLI output

### Data Flow

1. **Fetch Phase**
   - Read feed URLs from `feeds.yaml`
   - Fetch and parse RSS/Atom feeds
   - Extract article data (title, content, date, link, image)
   - Handle timezone conversions

2. **Process Phase**
   - Generate embeddings for article content
   - Assign topics using sentence-transformers
   - Store in SQLite database

3. **Generate Phase**
   - Query database for articles from enabled sources
   - Group by categories and topics
   - Render Jinja2 templates
   - Output static HTML to `/site`
   - Copy static assets

4. **Deploy Phase**
   - GitHub Actions commits changes to git
   - GitHub Pages serves updated site

### Database Schema

#### Articles Table
- id (primary key)
- url (unique)
- title
- content
- image_url
- published_date
- fetched_date
- source_id (foreign key)

#### Sources Table
- id (primary key)
- name
- feed_url (unique)
- website_url
- category
- enabled (boolean)
- last_fetched
- created_at

#### Topics Table
- id (primary key)
- name (unique)
- slug (unique)

#### ArticleTopics Table (junction)
- id (primary key)
- article_id (foreign key)
- topic_id (foreign key)

---

## Implementation Status

### Phase 1: Project Setup & Architecture ✅ COMPLETED

**Tasks Completed:**
- ✅ Create directory structure
- ✅ Create `pyproject.toml` with dependencies
- ✅ Create configuration files (`feeds.yaml`)
- ✅ Create Python package structure
- ✅ Create `.gitignore`
- ✅ Initialize git repository

### Phase 2: Core RSS Feed Processing ✅ COMPLETED

**Tasks Completed:**
- ✅ Create database models (SQLAlchemy)
- ✅ Implement RSS feed fetcher with error handling
- ✅ Parse and extract article data
- ✅ Image extraction from RSS and HTML content
- ✅ Timezone handling for date parsing
- ✅ Create database operations
- ✅ Build CLI command: `feedrr fetch`
- ✅ Add logging and monitoring
- ✅ Comprehensive test suite for fetcher

### Phase 3: LLM Integration ✅ COMPLETED

**Tasks Completed:**
- ✅ Download and load sentence-transformers model (all-MiniLM-L6-v2)
- ✅ Implement topic assignment using embeddings
- ✅ Store topic associations in database
- ✅ Content deduplication using cosine similarity (0.85 threshold)
- ✅ Duplicate tracking in database (embedding storage, is_duplicate flag)
- ✅ Article stacking - filter duplicates from UI
- ✅ Trending detection - badge for multi-source articles
- ✅ Expandable source list UI with individual links
- ✅ CLI tool: `feedrr process` with `--skip-dedup` option
- ✅ Comprehensive test suite for deduplication (17 tests)

### Phase 4: Static Site Generation ✅ COMPLETED

**Tasks Completed:**
- ✅ Design template structure (base.html, index.html)
- ✅ Implement static site generator
- ✅ Filter by enabled sources only
- ✅ Category and topic filtering UI
- ✅ Mobile-responsive dropdown filters
- ✅ Generate index with all articles
- ✅ Copy static assets
- ✅ CLI tool: `feedrr generate`

### Phase 5: Web UI ✅ COMPLETED

**Tasks Completed:**
- ✅ Create clean, minimal iOS-inspired UI
- ✅ Mobile-first responsive design
- ✅ Two-view toggle (list and card)
- ✅ List view: compact layout with image on right
- ✅ Card view: full-width image at top
- ✅ Category and topic filtering with dropdowns
- ✅ Compact source button inline with topic tags
- ✅ Fast loading with optimized CSS/JS
- ✅ localStorage for view preference

### Phase 6: GitHub Pages Deployment ✅ COMPLETED

**Tasks Completed:**
- ✅ Create GitHub Actions workflow
- ✅ Configure GitHub Pages
- ✅ Automated deployment on push to main
- ✅ Live site at jamiefletcher.dev/feedrr

### Post-MVP Enhancements (Planned)

**Deduplication & Trending:**
- [ ] Article stacking view for duplicates
- [ ] Trending topics detection
- [ ] Time-based trending indicators

**Enhanced Features:**
- [ ] Bionic reader mode
- [ ] Database versioning and rollback
- [ ] Web scraping for article images
- [ ] Search functionality
- [ ] Reading time estimates

---

## Technical Specifications

### Configuration Files

#### src/config/feeds.yaml
Configuration for RSS feed sources:

```yaml
- name: "Broadband TV News"
  feed_url: "http://feeds.feedburner.com/broadbandtvnews"
  enabled: true
  category: "ott news"

- name: "Streaming Media"
  feed_url: "https://www.streamingmedia.com/RSS/SMRSS.aspx"
  enabled: true
  category: "ott news"
```

### CLI Commands

```bash
# Fetch RSS feeds
feedrr fetch

# Process articles with LLM
feedrr process

# Generate static site
feedrr generate

# Full pipeline (fetch + process + generate)
feedrr build

# Initialize database
feedrr init-db
```

### UI Features

#### Two-View Toggle
- **List View** (default):
  - Compact layout with image on right (120x120px)
  - Title, source, date, preview text
  - Topics + Source button
  - Content hidden

- **Card View**:
  - Full-width image at top (200px height)
  - Source/date overlaid on image (top-right)
  - Title below image
  - Topics + Source button
  - Full content visible (if available)

#### Filtering
- **Category Filter**: Dropdown to filter by source category (e.g., "ott news")
- **Topic Filter**: Dropdown to filter by AI-assigned topics
- **Filter Status**: Shows active filters and article count
- Client-side filtering with JavaScript

#### Source Button
- Compact blue outline button
- Positioned inline with topic tags
- Hover effect: fills with blue, white text
- External link icon

---

## Error Handling

### Philosophy

The error handling follows these principles:

1. **Fail Gracefully**: Individual feed failures don't stop the pipeline
2. **Log and Continue**: Errors are logged but processing continues
3. **User Visibility**: Users see which feeds failed in output
4. **Idempotency**: Re-running commands is safe (duplicates skipped)

### RSS Feed Fetching Errors

#### Handled Cases:

1. **Rate Limiting (HTTP 420)**
   - Some feeds implement aggressive rate limiting
   - Error is logged, feed is skipped, other feeds continue

2. **HTTP Errors (4xx, 5xx)**
   - 404 Not Found, 500 Server Error, etc.
   - All HTTP errors are caught, logged, and skipped

3. **Network Timeouts**
   - Default timeout: 60 seconds
   - Timeout exceptions caught, feed skipped

4. **Parse Errors**
   - Malformed XML/RSS or encoding issues
   - Parse errors caught, feed skipped

5. **Timezone Warnings**
   - Unknown timezone abbreviations (EST, PST, etc.)
   - Handled with tzinfos mapping to UTC offsets

#### Implementation

```python
# Timezone handling
tzinfos = {
    'EST': -18000,  # UTC-5
    'EDT': -14400,  # UTC-4
    # ... more timezones
}

try:
    # Fetch and parse feed
    response = requests.get(feed_url, timeout=60)
    response.raise_for_status()
    # ... parse articles
except Exception as e:
    print(f"Error fetching {feed_url}: {e}")
    return []
```

### Database Errors

#### Handled Cases:

1. **Duplicate Articles**
   - Same URL fetched multiple times
   - Checked before insert, duplicates skipped

2. **Integrity Constraint Violations**
   - Transaction rolled back, error caught

```python
try:
    session.commit()
except IntegrityError:
    session.rollback()
    pass  # Duplicates handled gracefully
```

### Topic Processing Errors

1. **Empty Articles** → Assigned 'general' topic by default
2. **Model Loading Failures** → Process command fails (critical error)
3. **Unknown Topics** → Assignment skipped
4. **Duplicate Assignments** → Database constraint prevents duplicates

---

## Recent Updates

### Phase 3 Release (2025-12-07)

1. **Content Deduplication** ⭐ NEW
   - Automatic duplicate detection using AI embeddings
   - 85% similarity threshold for duplicate matching
   - Duplicate articles filtered from main feed
   - Comprehensive test suite with 17 tests

2. **Trending Detection** ⭐ NEW
   - Orange "Trending" badge for multi-source articles
   - Shows number of sources covering the story
   - Hover tooltip with source names

3. **Multi-Source Navigation** ⭐ NEW
   - Expandable "Sources" button for duplicated articles
   - Click to reveal all sources covering the story
   - Individual clickable links for each source
   - Smooth expand/collapse animation

4. **Two-View Toggle**
   - List view: compact with image on right
   - Card view: full-width image at top
   - LocalStorage preference saving

5. **UI Enhancements**
   - Compact source button inline with topic tags
   - Dropdown-based category and topic filtering
   - Mobile-responsive design
   - Clean card view layout

6. **Image Extraction**
   - Extract from RSS media:content
   - Fallback to HTML content parsing
   - WordPress content:encoded support

7. **Database Updates**
   - Added embedding storage (LargeBinary)
   - is_duplicate and duplicate_of_id fields
   - Self-referential relationship for duplicates

---

## Success Criteria

- ✅ Successfully fetch and parse RSS feeds from multiple sources
- ✅ Accurate topic tagging on articles
- ✅ Content deduplication (>85% similarity threshold)
- ✅ Clean, mobile-friendly UI
- ✅ Automated deployment to GitHub Pages
- ✅ Category and topic filtering
- ✅ Two responsive view modes
- ✅ Article stacking (duplicates filtered from feed)
- ✅ Trending detection (multi-source article badges)
- ✅ Comprehensive test coverage for core features

---

*Last Updated: 2025-12-07*
*Status: MVP Complete with Phase 3 Enhancements - All Core Features Implemented*
