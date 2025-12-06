"""Simple database operations for MVP."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Source, Article, Topic, ArticleTopic, get_session


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
            image_url=article_data.get('image_url'),
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


def load_topics_from_config(session: Session, topics_config: List[dict]) -> None:
    """Load topics from config into database."""
    for topic_data in topics_config:
        # Check if topic already exists
        existing = session.query(Topic).filter_by(slug=topic_data['slug']).first()
        if existing:
            # Update existing topic
            existing.name = topic_data['name']
        else:
            # Create new topic
            topic = Topic(
                name=topic_data['name'],
                slug=topic_data['slug']
            )
            session.add(topic)

    session.commit()


def get_articles_without_topics(session: Session) -> List[Article]:
    """Get articles that haven't been tagged yet."""
    # Get articles that have no topic assignments
    articles = session.query(Article).outerjoin(ArticleTopic).filter(
        ArticleTopic.id == None
    ).all()
    return articles


def assign_topic_to_article(session: Session, article: Article, topic_slug: str) -> None:
    """Assign a topic to an article."""
    # Get topic by slug
    topic = session.query(Topic).filter_by(slug=topic_slug).first()
    if not topic:
        # Create 'general' topic if it doesn't exist
        if topic_slug == 'general':
            topic = Topic(name='General', slug='general')
            session.add(topic)
            session.commit()
        else:
            return  # Skip unknown topics

    # Check if already assigned
    existing = session.query(ArticleTopic).filter_by(
        article_id=article.id,
        topic_id=topic.id
    ).first()

    if not existing:
        article_topic = ArticleTopic(
            article_id=article.id,
            topic_id=topic.id
        )
        session.add(article_topic)
        session.commit()
