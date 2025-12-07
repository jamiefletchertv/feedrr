"""Static site generator for feedrr."""

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session

from feedrr.storage.models import Article, Source, Topic, ArticleTopic
from feedrr.config import get_templates_dir, get_static_dir


def get_articles_with_topics(session: Session, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get articles with their topics and source information.

    Only returns articles from enabled sources.

    Returns list of article dictionaries with:
    - id, url, title, content
    - published_date (formatted string)
    - source_name
    - topics (list of topic names)
    """
    articles = []

    # Query articles with sources, filtered by enabled sources, ordered by published date (most recent first)
    query = session.query(Article).join(Source).filter(
        Source.enabled == True
    ).order_by(
        Article.published_date.desc().nullslast(),
        Article.fetched_date.desc()
    ).limit(limit)

    for article in query:
        # Get topics for this article
        topic_names = []
        for article_topic in article.topics:
            if article_topic.topic:
                topic_names.append(article_topic.topic.name)

        # Format published date
        if article.published_date:
            published_str = article.published_date.strftime("%b %d, %Y")
        else:
            published_str = article.fetched_date.strftime("%b %d, %Y")

        # Clean content - remove if it's just "Comments" or HTML links
        clean_content = None
        if article.content:
            # Strip HTML tags
            text_content = re.sub(r'<[^>]+>', '', article.content).strip()
            # Only include if it's meaningful (not just "Comments")
            if text_content and text_content.lower() != 'comments' and len(text_content) > 20:
                clean_content = text_content

        articles.append({
            'id': article.id,
            'url': article.url,
            'title': article.title,
            'content': clean_content,
            'image_url': article.image_url,
            'published_date': published_str,
            'source_name': article.source.name,
            'source_category': article.source.category,
            'topics': sorted(topic_names)  # Sort for consistent display
        })

    return articles


def generate_site(session: Session, output_dir: Path, max_articles: int = 100) -> None:
    """
    Generate static site from database.

    Args:
        session: Database session
        output_dir: Output directory for generated site
        max_articles: Maximum number of articles to include
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set up Jinja2 environment
    templates_dir = get_templates_dir()
    env = Environment(loader=FileSystemLoader(str(templates_dir)))

    # Get articles with topics
    articles = get_articles_with_topics(session, limit=max_articles)

    # Collect unique categories and topics for filters
    categories = set()
    all_topics = set()
    for article in articles:
        if article.get('source_category'):
            categories.add(article['source_category'])
        all_topics.update(article.get('topics', []))

    # Render index page
    template = env.get_template('index.html')
    html = template.render(
        articles=articles,
        categories=sorted(categories),
        topics=sorted(all_topics),
        last_updated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    )

    # Write index.html
    index_path = output_dir / 'index.html'
    index_path.write_text(html)

    # Copy static assets
    static_src = get_static_dir()
    static_dest = output_dir / 'static'

    # Remove existing static directory if it exists
    if static_dest.exists():
        shutil.rmtree(static_dest)

    # Copy static files
    if static_src.exists():
        shutil.copytree(static_src, static_dest)
