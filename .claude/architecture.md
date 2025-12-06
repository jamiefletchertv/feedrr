# feedrr - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (Scheduler)                │
│                    Runs every 30-60 minutes                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RSS Feed Fetcher                          │
│  - Fetch feeds from configured sources                      │
│  - Parse RSS/Atom feeds                                      │
│  - Extract articles (title, content, date, link)            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Processor                             │
│  - Topic Tagging (sentence-transformers)                    │
│  - Content Deduplication (embedding similarity)             │
│  - Lightweight local processing                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│  - Store articles with metadata                             │
│  - Track topics and tags                                    │
│  - Mark duplicates                                           │
│  - Version control support                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Static Site Generator                       │
│  - Jinja2 templates                                          │
│  - Generate HTML pages                                       │
│  - Create index, topic pages, article pages                 │
│  - Output to /docs folder                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Pages                             │
│  - Serve static files from /docs                            │
│  - Mobile-responsive UI                                      │
│  - Fast loading (pre-generated)                              │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
feedrr/
├── .claude/              # Project documentation for LLM context
│   ├── project-overview.md
│   ├── architecture.md
│   ├── implementation-phases.md
│   └── technical-specs.md
│
├── src/                  # Source code
│   ├── fetcher/         # RSS feed fetching logic
│   ├── processor/       # LLM processing (tagging, dedup)
│   ├── storage/         # Database operations
│   └── generator/       # Static site generation
│
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── article.html
│   └── topic.html
│
├── static/              # CSS/JS assets
│   ├── css/
│   └── js/
│
├── data/                # SQLite database
│   └── feedrr.db
│
├── docs/                # Project documentation
│   └── DEVELOPMENT.md
│
├── site/                # Generated static site (GitHub Pages)
│   └── (generated files)
│
├── feeds.yaml           # RSS feed configuration
├── config.yaml          # Application configuration
├── pyproject.toml       # Python project configuration
└── README.md            # Project README
```

## Technology Stack

### Core Dependencies
- **feedparser** - RSS/Atom feed parsing
- **requests** - HTTP requests for fetching feeds
- **python-dateutil** - Date parsing and handling

### LLM & NLP
- **sentence-transformers** - Lightweight embedding model
- **torch** - PyTorch backend for transformers
- **numpy** - Numerical operations

### Database
- **SQLAlchemy** - Database ORM
- **SQLite** - Embedded database

### Static Site Generation
- **Jinja2** - Template engine
- **markdown** - Markdown to HTML conversion
- **PyYAML** - Configuration file parsing

### Utilities
- **click** - CLI framework
- **python-dotenv** - Environment variable management
- **rich** - Beautiful CLI output

## Data Flow

1. **Fetch Phase**
   - Read feed URLs from `feeds.yaml`
   - Fetch and parse RSS/Atom feeds
   - Extract article data

2. **Process Phase**
   - Generate embeddings for article content
   - Compare with existing articles for deduplication
   - Assign topics using zero-shot classification
   - Store in SQLite database

3. **Generate Phase**
   - Query database for articles
   - Render Jinja2 templates
   - Output static HTML to `/site`
   - Copy static assets

4. **Deploy Phase**
   - GitHub Actions commits changes to git
   - GitHub Pages serves updated site

## LLM Processing Details

### Topic Tagging
- **Model**: all-MiniLM-L6-v2 (80MB, sentence-transformers)
- **Method**: Zero-shot classification or embedding clustering
- **Topics**: Tech, Politics, Science, Business, Sports, Entertainment, etc.
- **Storage**: Many-to-many relationship (article can have multiple topics)

### Content Deduplication
- **Method**: Cosine similarity on content embeddings
- **Threshold**: 0.85 similarity = duplicate
- **Strategy**: Keep earliest article, mark duplicates
- **Edge cases**: Different sources reporting same news

## Database Schema

### Articles Table
- id (primary key)
- url (unique)
- title
- content
- summary
- published_date
- fetched_date
- source_id (foreign key)
- is_duplicate (boolean)
- duplicate_of_id (foreign key, nullable)
- embedding (blob, serialized numpy array)

### Sources Table
- id (primary key)
- name
- feed_url
- website_url
- last_fetched
- fetch_count
- error_count

### Topics Table
- id (primary key)
- name
- slug
- description

### ArticleTopics Table (junction)
- article_id (foreign key)
- topic_id (foreign key)
- confidence_score

## Performance Considerations

- **Incremental Processing**: Only process new articles
- **Embedding Cache**: Store embeddings to avoid recomputation
- **Batch Processing**: Process multiple articles together
- **Lazy Loading**: Load LLM model only when needed
- **Static Output**: Pre-generate all HTML for fast page loads
