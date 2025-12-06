# feedrr - Technical Specifications

## Configuration Files

### feeds.yaml
Configuration for RSS feed sources.

```yaml
sources:
  - name: "Hacker News"
    feed_url: "https://news.ycombinator.com/rss"
    website_url: "https://news.ycombinator.com"
    enabled: true
    category: "tech"

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

### config.yaml
Application configuration.

```yaml
app:
  name: "feedrr"
  version: "0.1.0"
  timezone: "UTC"

database:
  path: "data/feedrr.db"
  backup_enabled: true
  backup_count: 7

llm:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"
  model_cache_dir: "data/models"
  dedup_threshold: 0.85
  batch_size: 32

topics:
  - name: "Technology"
    slug: "tech"
    keywords: ["software", "hardware", "ai", "programming"]
  - name: "Science"
    slug: "science"
    keywords: ["research", "study", "discovery"]
  - name: "Business"
    slug: "business"
    keywords: ["market", "company", "economy"]
  - name: "Politics"
    slug: "politics"
    keywords: ["government", "election", "policy"]

fetcher:
  timeout: 30
  retry_attempts: 3
  retry_delay: 5
  user_agent: "feedrr/0.1.0 (+https://github.com/youruser/feedrr)"

generator:
  output_dir: "docs"
  articles_per_page: 20
  recent_articles_count: 50
  static_dirs: ["static"]

deployment:
  schedule_cron: "*/30 * * * *"  # Every 30 minutes
  commit_author: "feedrr-bot"
  commit_email: "bot@feedrr.local"
```

## Database Schema (SQLAlchemy Models)

### models.py

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    feed_url = Column(String(500), unique=True, nullable=False)
    website_url = Column(String(500))
    category = Column(String(100))
    enabled = Column(Boolean, default=True)
    last_fetched = Column(DateTime)
    fetch_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    last_error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship("Article", back_populates="source")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    url = Column(String(1000), unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    summary = Column(Text)
    author = Column(String(255))
    published_date = Column(DateTime)
    fetched_date = Column(DateTime, default=datetime.utcnow)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)

    # Deduplication
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    embedding = Column(LargeBinary)  # Serialized numpy array

    # Relationships
    source = relationship("Source", back_populates="articles")
    topics = relationship("ArticleTopic", back_populates="article")
    duplicate_of = relationship("Article", remote_side=[id], backref="duplicates")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship("ArticleTopic", back_populates="topic")

class ArticleTopic(Base):
    __tablename__ = "article_topics"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    confidence_score = Column(Float, default=0.0)
    assigned_date = Column(DateTime, default=datetime.utcnow)

    article = relationship("Article", back_populates="topics")
    topic = relationship("Topic", back_populates="articles")
```

## API/CLI Interface

### CLI Commands

```bash
# Fetch RSS feeds
feedrr fetch [--source <name>] [--all]

# Process articles with LLM
feedrr process [--reprocess] [--limit <n>]

# Generate static site
feedrr generate [--force] [--output <dir>]

# Full pipeline (fetch + process + generate)
feedrr build

# Initialize database
feedrr init-db

# Show statistics
feedrr stats

# List configured sources
feedrr sources list

# Add new source
feedrr sources add <name> <feed_url>

# Clean up old articles
feedrr cleanup [--days <n>]
```

## LLM Processing Algorithms

### Topic Tagging Algorithm

```python
def assign_topics(article_text: str, topics: List[Topic]) -> List[Tuple[Topic, float]]:
    """
    Assign topics to article using zero-shot classification.

    Args:
        article_text: Article content
        topics: List of available topics

    Returns:
        List of (topic, confidence_score) tuples
    """
    # Generate embedding for article
    article_embedding = model.encode(article_text)

    # Compare with topic keywords/descriptions
    results = []
    for topic in topics:
        topic_text = f"{topic.name} {topic.description}"
        topic_embedding = model.encode(topic_text)

        # Calculate cosine similarity
        similarity = cosine_similarity(article_embedding, topic_embedding)

        if similarity > 0.3:  # Threshold
            results.append((topic, similarity))

    # Return top topics
    return sorted(results, key=lambda x: x[1], reverse=True)[:3]
```

### Deduplication Algorithm

```python
def find_duplicates(new_article: Article, existing_articles: List[Article]) -> Optional[Article]:
    """
    Find if new article is duplicate of existing articles.

    Args:
        new_article: Newly fetched article
        existing_articles: Articles from database

    Returns:
        Original article if duplicate found, None otherwise
    """
    new_embedding = model.encode(new_article.content)

    for existing in existing_articles:
        existing_embedding = deserialize_embedding(existing.embedding)
        similarity = cosine_similarity(new_embedding, existing_embedding)

        if similarity > 0.85:  # Duplicate threshold
            return existing

    return None
```

## Template Structure

### base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}feedrr{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
    <header>
        <nav>
            <h1>feedrr</h1>
            <button id="theme-toggle">🌙</button>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>Generated by feedrr • Last updated: {{ last_updated }}</p>
    </footer>

    <script src="/static/js/main.js"></script>
</body>
</html>
```

## GitHub Actions Workflow

### .github/workflows/build.yml

```yaml
name: Build and Deploy

on:
  schedule:
    - cron: '*/30 * * * *'  # Every 30 minutes
  workflow_dispatch:  # Manual trigger
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .

      - name: Run full build
        run: feedrr build

      - name: Commit changes
        run: |
          git config --local user.email "bot@feedrr.local"
          git config --local user.name "feedrr-bot"
          git add docs/ data/
          git diff --quiet && git diff --staged --quiet || git commit -m "Update feed: $(date)"

      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Performance Targets

- Feed fetch: < 5 seconds per feed
- LLM processing: < 100ms per article (batch mode)
- Static site generation: < 30 seconds for 1000 articles
- Page load time: < 1 second (static files)
- Mobile performance: Lighthouse score > 90

## Security Considerations

- Sanitize HTML content from RSS feeds (XSS prevention)
- Validate URLs before fetching
- Rate limiting for external requests
- No user authentication needed (static site)
- HTTPS only for GitHub Pages
