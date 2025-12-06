"""Tests for database topic operations."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from feedrr.storage.models import Base, Source, Article, Topic, ArticleTopic
from feedrr.storage.db import (
    load_topics_from_config,
    get_articles_without_topics,
    assign_topic_to_article
)


@pytest.fixture
def db_session():
    """Create an in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()


@pytest.fixture
def sample_source(db_session):
    """Create a sample source."""
    source = Source(
        name="Test Source",
        feed_url="https://example.com/feed.xml"
    )
    db_session.add(source)
    db_session.commit()
    return source


def test_load_topics_from_config(db_session):
    """Test loading topics from config."""
    topics_config = [
        {"name": "Technology", "slug": "tech"},
        {"name": "Science", "slug": "science"},
    ]

    load_topics_from_config(db_session, topics_config)

    # Verify topics were created
    topics = db_session.query(Topic).all()
    assert len(topics) == 2
    assert topics[0].name == "Technology"
    assert topics[0].slug == "tech"
    assert topics[1].name == "Science"
    assert topics[1].slug == "science"


def test_load_topics_update_existing(db_session):
    """Test that loading topics updates existing ones."""
    # Create initial topic
    topic = Topic(name="Tech", slug="tech")
    db_session.add(topic)
    db_session.commit()

    # Update with new name
    topics_config = [
        {"name": "Technology", "slug": "tech"},
    ]

    load_topics_from_config(db_session, topics_config)

    # Verify topic was updated, not duplicated
    topics = db_session.query(Topic).all()
    assert len(topics) == 1
    assert topics[0].name == "Technology"
    assert topics[0].slug == "tech"


def test_get_articles_without_topics(db_session, sample_source):
    """Test getting articles without topic assignments."""
    # Create articles
    article1 = Article(
        url="https://example.com/1",
        title="Article 1",
        source_id=sample_source.id
    )
    article2 = Article(
        url="https://example.com/2",
        title="Article 2",
        source_id=sample_source.id
    )
    db_session.add(article1)
    db_session.add(article2)
    db_session.commit()

    # Create topic and assign to article1
    topic = Topic(name="Tech", slug="tech")
    db_session.add(topic)
    db_session.commit()

    article_topic = ArticleTopic(
        article_id=article1.id,
        topic_id=topic.id
    )
    db_session.add(article_topic)
    db_session.commit()

    # Get articles without topics
    articles = get_articles_without_topics(db_session)

    # Should only return article2
    assert len(articles) == 1
    assert articles[0].id == article2.id


def test_get_articles_without_topics_empty(db_session):
    """Test getting articles when none exist."""
    articles = get_articles_without_topics(db_session)
    assert len(articles) == 0


def test_assign_topic_to_article(db_session, sample_source):
    """Test assigning a topic to an article."""
    # Create article
    article = Article(
        url="https://example.com/1",
        title="Test Article",
        source_id=sample_source.id
    )
    db_session.add(article)
    db_session.commit()

    # Create topic
    topic = Topic(name="Tech", slug="tech")
    db_session.add(topic)
    db_session.commit()

    # Assign topic
    assign_topic_to_article(db_session, article, "tech")

    # Verify assignment
    article_topics = db_session.query(ArticleTopic).filter_by(article_id=article.id).all()
    assert len(article_topics) == 1
    assert article_topics[0].topic_id == topic.id


def test_assign_topic_creates_general(db_session, sample_source):
    """Test that assigning 'general' topic creates it if missing."""
    # Create article
    article = Article(
        url="https://example.com/1",
        title="Test Article",
        source_id=sample_source.id
    )
    db_session.add(article)
    db_session.commit()

    # Assign general topic (doesn't exist yet)
    assign_topic_to_article(db_session, article, "general")

    # Verify general topic was created
    general_topic = db_session.query(Topic).filter_by(slug="general").first()
    assert general_topic is not None
    assert general_topic.name == "General"

    # Verify assignment
    article_topics = db_session.query(ArticleTopic).filter_by(article_id=article.id).all()
    assert len(article_topics) == 1
    assert article_topics[0].topic_id == general_topic.id


def test_assign_unknown_topic(db_session, sample_source):
    """Test that assigning unknown topic is skipped."""
    # Create article
    article = Article(
        url="https://example.com/1",
        title="Test Article",
        source_id=sample_source.id
    )
    db_session.add(article)
    db_session.commit()

    # Try to assign unknown topic
    assign_topic_to_article(db_session, article, "unknown")

    # Verify no assignment was made
    article_topics = db_session.query(ArticleTopic).filter_by(article_id=article.id).all()
    assert len(article_topics) == 0


def test_assign_duplicate_topic(db_session, sample_source):
    """Test that assigning the same topic twice doesn't create duplicates."""
    # Create article and topic
    article = Article(
        url="https://example.com/1",
        title="Test Article",
        source_id=sample_source.id
    )
    topic = Topic(name="Tech", slug="tech")
    db_session.add(article)
    db_session.add(topic)
    db_session.commit()

    # Assign topic twice
    assign_topic_to_article(db_session, article, "tech")
    assign_topic_to_article(db_session, article, "tech")

    # Verify only one assignment exists
    article_topics = db_session.query(ArticleTopic).filter_by(article_id=article.id).all()
    assert len(article_topics) == 1


def test_assign_multiple_topics(db_session, sample_source):
    """Test assigning multiple topics to one article."""
    # Create article
    article = Article(
        url="https://example.com/1",
        title="Test Article",
        source_id=sample_source.id
    )
    db_session.add(article)
    db_session.commit()

    # Create topics
    topic1 = Topic(name="Tech", slug="tech")
    topic2 = Topic(name="Science", slug="science")
    db_session.add(topic1)
    db_session.add(topic2)
    db_session.commit()

    # Assign both topics
    assign_topic_to_article(db_session, article, "tech")
    assign_topic_to_article(db_session, article, "science")

    # Verify both assignments
    article_topics = db_session.query(ArticleTopic).filter_by(article_id=article.id).all()
    assert len(article_topics) == 2

    topic_ids = {at.topic_id for at in article_topics}
    assert topic1.id in topic_ids
    assert topic2.id in topic_ids
