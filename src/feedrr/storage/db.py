"""Simple database operations for MVP."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Source, Article, get_session


def load_sources_from_config(session: Session, sources_config: List[dict]) -> None:
    """Load sources from config into database."""
    for source_data in sources_config:
        # Check if source already exists
        existing = session.query(Source).filter_by(feed_url=source_data['feed_url']).first()
        if existing:
            # Update existing source
            existing.name = source_data['name']
            existing.website_url = source_data.get('website_url')
            existing.enabled = source_data.get('enabled', True)
        else:
            # Create new source
            source = Source(
                name=source_data['name'],
                feed_url=source_data['feed_url'],
                website_url=source_data.get('website_url'),
                enabled=source_data.get('enabled', True)
            )
            session.add(source)

    session.commit()


def get_enabled_sources(session: Session) -> List[Source]:
    """Get all enabled sources."""
    return session.query(Source).filter_by(enabled=True).all()


def save_articles(session: Session, source: Source, articles_data: List[dict]) -> int:
    """
    Save articles to database.

    Returns number of new articles saved (duplicates skipped).
    """
    saved_count = 0

    for article_data in articles_data:
        # Check if article already exists (by URL)
        existing = session.query(Article).filter_by(url=article_data['url']).first()
        if existing:
            continue  # Skip duplicates

        # Create new article
        article = Article(
            url=article_data['url'],
            title=article_data['title'],
            content=article_data.get('content'),
            published_date=article_data.get('published_date'),
            source_id=source.id
        )
        session.add(article)
        saved_count += 1

    # Update source last_fetched timestamp
    source.last_fetched = datetime.utcnow()

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        # Some duplicates might have been added between queries
        pass

    return saved_count


def get_article_count(session: Session) -> int:
    """Get total article count."""
    return session.query(Article).count()


def get_source_count(session: Session) -> int:
    """Get total source count."""
    return session.query(Source).count()
