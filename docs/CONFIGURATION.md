# Configuration Guide

feedrr uses two YAML configuration files to manage the application behavior and RSS feed sources.

## config.yaml - Application Configuration

The `config.yaml` file controls **how feedrr operates**. It defines settings for all components of the application.

### Purpose
- Configure application behavior (not what feeds to fetch, but how to fetch/process them)
- Set LLM model parameters
- Define topic taxonomy for article classification
- Control static site generation
- Manage deployment settings

### File Location
`src/config/config.yaml`

### Structure

```yaml
app:
  name: "feedrr"              # Application name
  version: "0.1.0"            # Version number
  timezone: "UTC"             # Timezone for date handling

database:
  path: "data/feedrr.db"      # SQLite database location
  backup_enabled: true         # Enable automatic backups
  backup_count: 7              # Number of backups to keep

llm:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"  # HuggingFace model
  model_cache_dir: "data/models"                        # Where to cache model
  dedup_threshold: 0.85                                  # Similarity threshold (0-1)
  batch_size: 32                                         # Articles per batch

topics:
  - name: "Technology"        # Topic display name
    slug: "tech"              # URL-friendly identifier
    keywords: ["software", "hardware", "ai", "programming"]
  - name: "Science"
    slug: "science"
    keywords: ["research", "study", "discovery"]
  # Add more topics as needed...

fetcher:
  timeout: 30                 # HTTP request timeout (seconds)
  retry_attempts: 3           # Number of retry attempts on failure
  retry_delay: 5              # Delay between retries (seconds)
  user_agent: "feedrr/0.1.0 (+https://github.com/jamiefletchertv/feedrr)"
  max_articles_per_feed: 50   # Limit articles per feed per fetch

generator:
  output_dir: "site"          # Where to generate static files
  articles_per_page: 20       # Pagination size
  recent_articles_count: 50   # Number of recent articles on homepage
  static_dirs: ["static"]     # Directories to copy to output
  max_summary_length: 300     # Max characters for article summaries

deployment:
  schedule_cron: "*/30 * * * *"       # GitHub Actions schedule
  commit_author: "feedrr-bot"         # Git commit author name
  commit_email: "bot@feedrr.local"    # Git commit author email
```

### When to Edit config.yaml

**Edit when you want to:**
- Change LLM model or parameters
- Adjust deduplication sensitivity
- Add/remove/modify topic categories
- Change how many articles to display
- Modify retry behavior for failed feeds
- Adjust GitHub Actions schedule
- Change pagination settings

**Don't edit for:**
- Adding new RSS feeds (use `feeds.yaml` instead)
- Enabling/disabling specific feeds (use `feeds.yaml` instead)

---

## feeds.yaml - RSS Feed Sources

The `feeds.yaml` file defines **which RSS feeds to fetch**. It's a list of RSS/Atom feed URLs to monitor.

### Purpose
- Define RSS feed sources to aggregate
- Enable/disable individual feeds
- Categorize feeds
- Store feed metadata

### File Location
`src/config/feeds.yaml`

### Structure

```yaml
sources:
  - name: "Hacker News"                           # Display name for the source
    feed_url: "https://news.ycombinator.com/rss"  # RSS/Atom feed URL
    website_url: "https://news.ycombinator.com"   # Main website URL
    enabled: true                                  # Whether to fetch this feed
    category: "tech"                               # Optional category tag

  - name: "TechCrunch"
    feed_url: "https://techcrunch.com/feed/"
    website_url: "https://techcrunch.com"
    enabled: true
    category: "tech"

  - name: "The Verge"
    feed_url: "https://www.theverge.com/rss/index.xml"
    website_url: "https://www.theverge.com"
    enabled: true
    category: "tech"
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Human-readable name for the feed source |
| `feed_url` | Yes | Full URL to the RSS/Atom feed |
| `website_url` | No | Main website URL (used for attribution) |
| `enabled` | No | Set to `false` to temporarily disable (default: `true`) |
| `category` | No | Category tag for organization |

### When to Edit feeds.yaml

**Add a new feed:**
```yaml
sources:
  - name: "My Favorite Blog"
    feed_url: "https://example.com/feed.xml"
    website_url: "https://example.com"
    enabled: true
    category: "blogs"
```

**Disable a feed temporarily:**
```yaml
sources:
  - name: "Hacker News"
    feed_url: "https://news.ycombinator.com/rss"
    website_url: "https://news.ycombinator.com"
    enabled: false  # ← Change to false
    category: "tech"
```

**Remove a feed permanently:**
Delete the entire entry from the list.

### Finding RSS Feeds

Most websites have RSS feeds. Common locations:
- `/rss`
- `/feed`
- `/feed.xml`
- `/atom.xml`
- `/rss.xml`

Look for RSS icon (🟠) in browser, or view page source for `<link rel="alternate" type="application/rss+xml">`.

### CLI Commands for Feed Management

```bash
# List all configured sources
feedrr sources list

# Add a new source
feedrr sources add "Blog Name" "https://example.com/feed.xml"
```

---

## Quick Comparison

| What You Want To Do | Which File |
|---------------------|------------|
| Add a new blog to follow | `feeds.yaml` |
| Change article deduplication threshold | `config.yaml` |
| Disable a specific feed | `feeds.yaml` |
| Add a new topic category | `config.yaml` |
| Change how often GitHub Actions runs | `config.yaml` |
| Change LLM model | `config.yaml` |
| Temporarily stop fetching from a source | `feeds.yaml` (set `enabled: false`) |
| Adjust how many articles show per page | `config.yaml` |

---

## Example Use Cases

### Use Case 1: Following More Tech News
**Goal:** Add Ars Technica to your feed

**Edit:** `feeds.yaml`
```yaml
sources:
  # ... existing feeds ...
  - name: "Ars Technica"
    feed_url: "http://feeds.arstechnica.com/arstechnica/index"
    website_url: "https://arstechnica.com"
    enabled: true
    category: "tech"
```

### Use Case 2: More Aggressive Deduplication
**Goal:** Catch more duplicate articles (even if they're slightly different)

**Edit:** `config.yaml`
```yaml
llm:
  dedup_threshold: 0.75  # Lower = more aggressive (was 0.85)
```

### Use Case 3: Run Updates Hourly Instead of Every 30 Minutes
**Goal:** Reduce GitHub Actions usage

**Edit:** `config.yaml`
```yaml
deployment:
  schedule_cron: "0 * * * *"  # Every hour at minute 0
```

### Use Case 4: Add Sports Coverage
**Goal:** Track sports news with proper categorization

**Step 1:** Add topic to `config.yaml`
```yaml
topics:
  # ... existing topics ...
  - name: "Sports"
    slug: "sports"
    keywords: ["game", "team", "player", "score", "championship"]
```

**Step 2:** Add feeds to `feeds.yaml`
```yaml
sources:
  # ... existing sources ...
  - name: "ESPN"
    feed_url: "https://www.espn.com/espn/rss/news"
    website_url: "https://espn.com"
    enabled: true
    category: "sports"
```

---

## Validation

### Checking Your Configuration

Before deploying, validate your YAML files:

```bash
# Python YAML validation
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
python -c "import yaml; yaml.safe_load(open('feeds.yaml'))"
```

### Common Mistakes

❌ **Bad YAML syntax:**
```yaml
sources:
- name: "Missing quotes on URL
  feed_url: https://example.com  # Might cause issues
```

✅ **Good YAML syntax:**
```yaml
sources:
  - name: "Proper quotes"
    feed_url: "https://example.com"
```

❌ **Wrong indentation:**
```yaml
sources:
- name: "Test"
feed_url: "https://example.com"  # Should be indented
```

✅ **Correct indentation:**
```yaml
sources:
  - name: "Test"
    feed_url: "https://example.com"  # Properly indented
```

---

## Environment-Specific Configuration

For local development vs. production, you can:

1. Use different config files:
   ```bash
   feedrr --config config.dev.yaml build
   ```

2. Override with environment variables (coming in Phase 2)
   ```bash
   export FEEDRR_LLM_MODEL="different-model"
   ```

3. Use `.env` file for secrets (coming in Phase 2)

---

## Further Reading

- [YAML Syntax Guide](https://yaml.org/spec/1.2.2/)
- [RSS Feed Discovery](https://www.rssboard.org/rss-specification)
- [Cron Expression Reference](https://crontab.guru/)
