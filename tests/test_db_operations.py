"""Tests for database operations."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from feedrr.storage.models import Base, Source, Article
from feedrr.storage.db import (
    load_sources_from_config,
    get_enabled_sources,
    save_articles,
    get_article_count,
    get_source_count
)


@pytest.fixture
def db_session():
    """Create an in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()


def test_load_sources_from_config(db_session):
    """Test loading sources from config."""
    sources_config = [
        {
            'name': 'Test Source 1',
            'feed_url': 'https://example.com/feed1.xml',
            'website_url': 'https://example.com',
            'enabled': True
        },
        {
            'name': 'Test Source 2',
            'feed_url': 'https://example.com/feed2.xml',
            'enabled': False
        }
    ]

    load_sources_from_config(db_session, sources_config)

    # Verify
    sources = db_session.query(Source).all()
    assert len(sources) == 2
    assert sources[0].name == 'Test Source 1'
    assert sources[0].enabled is True
    assert sources[1].enabled is False


def test_load_sources_from_config_update_existing(db_session):
    """Test that loading sources updates existing ones."""
    # Create initial source
    source = Source(
        name='Old Name',
        feed_url='https://example.com/feed.xml',
        enabled=False
    )
    db_session.add(source)
    db_session.commit()

    # Update via config
    sources_config = [
        {
            'name': 'New Name',
            'feed_url': 'https://example.com/feed.xml',
            'enabled': True
        }
    ]
    load_sources_from_config(db_session, sources_config)

    # Verify updated
    sources = db_session.query(Source).all()
    assert len(sources) == 1
    assert sources[0].name == 'New Name'
    assert sources[0].enabled is True


def test_get_enabled_sources(db_session):
    """Test getting only enabled sources."""
    source1 = Source(name='Enabled', feed_url='https://example.com/1', enabled=True)
    source2 = Source(name='Disabled', feed_url='https://example.com/2', enabled=False)
    source3 = Source(name='Also Enabled', feed_url='https://example.com/3', enabled=True)

    db_session.add_all([source1, source2, source3])
    db_session.commit()

    enabled = get_enabled_sources(db_session)
    assert len(enabled) == 2
    assert all(s.enabled for s in enabled)


def test_save_articles(db_session):
    """Test saving articles."""
    source = Source(name='Test', feed_url='https://example.com/feed.xml')
    db_session.add(source)
    db_session.commit()

    articles_data = [
        {
            'url': 'https://example.com/1',
            'title': 'Article 1',
            'content': 'Content 1',
            'published_date': None
        },
        {
            'url': 'https://example.com/2',
            'title': 'Article 2',
            'content': 'Content 2',
            'published_date': None
        }
    ]

    count = save_articles(db_session, source, articles_data)

    assert count == 2
    articles = db_session.query(Article).all()
    assert len(articles) == 2


def test_save_articles_skips_duplicates(db_session):
    """Test that duplicate articles are skipped."""
    source = Source(name='Test', feed_url='https://example.com/feed.xml')
    db_session.add(source)
    db_session.commit()

    # Save initial articles
    articles_data = [
        {'url': 'https://example.com/1', 'title': 'Article 1'},
        {'url': 'https://example.com/2', 'title': 'Article 2'}
    ]
    count1 = save_articles(db_session, source, articles_data)
    assert count1 == 2

    # Try to save same articles again
    count2 = save_articles(db_session, source, articles_data)
    assert count2 == 0  # Should skip all

    # Verify still only 2 articles
    articles = db_session.query(Article).all()
    assert len(articles) == 2


def test_save_articles_updates_last_fetched(db_session):
    """Test that save_articles updates source.last_fetched."""
    source = Source(name='Test', feed_url='https://example.com/feed.xml')
    db_session.add(source)
    db_session.commit()

    assert source.last_fetched is None

    articles_data = [
        {'url': 'https://example.com/1', 'title': 'Article 1'}
    ]
    save_articles(db_session, source, articles_data)

    db_session.refresh(source)
    assert source.last_fetched is not None


def test_get_article_count(db_session):
    """Test getting article count."""
    source = Source(name='Test', feed_url='https://example.com/feed.xml')
    db_session.add(source)
    db_session.commit()

    assert get_article_count(db_session) == 0

    article1 = Article(url='https://example.com/1', title='A1', source_id=source.id)
    article2 = Article(url='https://example.com/2', title='A2', source_id=source.id)
    db_session.add_all([article1, article2])
    db_session.commit()

    assert get_article_count(db_session) == 2


def test_get_source_count(db_session):
    """Test getting source count."""
    assert get_source_count(db_session) == 0

    source1 = Source(name='S1', feed_url='https://example.com/1')
    source2 = Source(name='S2', feed_url='https://example.com/2')
    db_session.add_all([source1, source2])
    db_session.commit()

    assert get_source_count(db_session) == 2
