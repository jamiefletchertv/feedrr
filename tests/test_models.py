"""Tests for database models."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from feedrr.storage.models import Base, Source, Article


@pytest.fixture
def db_session():
    """Create an in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()


def test_create_source(db_session):
    """Test creating a source."""
    source = Source(
        name="Test Source",
        feed_url="https://example.com/feed.xml",
        website_url="https://example.com",
        enabled=True
    )
    db_session.add(source)
    db_session.commit()

    # Verify
    assert source.id is not None
    assert source.name == "Test Source"
    assert source.enabled is True


def test_create_article(db_session):
    """Test creating an article."""
    # Create source first
    source = Source(
        name="Test Source",
        feed_url="https://example.com/feed.xml"
    )
    db_session.add(source)
    db_session.commit()

    # Create article
    article = Article(
        url="https://example.com/article1",
        title="Test Article",
        content="This is test content",
        source_id=source.id
    )
    db_session.add(article)
    db_session.commit()

    # Verify
    assert article.id is not None
    assert article.title == "Test Article"
    assert article.source_id == source.id


def test_article_source_relationship(db_session):
    """Test the relationship between articles and sources."""
    source = Source(
        name="Test Source",
        feed_url="https://example.com/feed.xml"
    )
    db_session.add(source)
    db_session.commit()

    article = Article(
        url="https://example.com/article1",
        title="Test Article",
        source_id=source.id
    )
    db_session.add(article)
    db_session.commit()

    # Test relationship
    assert article.source.name == "Test Source"
    assert len(source.articles) == 1
    assert source.articles[0].title == "Test Article"


def test_unique_article_url(db_session):
    """Test that article URLs must be unique."""
    source = Source(
        name="Test Source",
        feed_url="https://example.com/feed.xml"
    )
    db_session.add(source)
    db_session.commit()

    # Create first article
    article1 = Article(
        url="https://example.com/article1",
        title="Article 1",
        source_id=source.id
    )
    db_session.add(article1)
    db_session.commit()

    # Try to create duplicate
    article2 = Article(
        url="https://example.com/article1",  # Same URL
        title="Article 2",
        source_id=source.id
    )
    db_session.add(article2)

    # Should raise integrity error
    with pytest.raises(Exception):
        db_session.commit()


def test_unique_feed_url(db_session):
    """Test that feed URLs must be unique."""
    source1 = Source(
        name="Source 1",
        feed_url="https://example.com/feed.xml"
    )
    db_session.add(source1)
    db_session.commit()

    # Try to create duplicate
    source2 = Source(
        name="Source 2",
        feed_url="https://example.com/feed.xml"  # Same URL
    )
    db_session.add(source2)

    # Should raise integrity error
    with pytest.raises(Exception):
        db_session.commit()
