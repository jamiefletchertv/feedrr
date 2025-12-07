"""Tests for RSS fetcher."""

import pytest
from unittest.mock import Mock, patch
from feedrr.fetcher.rss import fetch_feed


def test_fetch_feed_success():
    """Test successful RSS feed fetch."""
    # Mock RSS feed content
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <item>
                <title>Test Article</title>
                <link>https://example.com/article1</link>
                <description>Test description</description>
                <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 1
    assert articles[0]['title'] == "Test Article"
    assert articles[0]['url'] == "https://example.com/article1"
    assert articles[0]['content'] == "Test description"


def test_fetch_feed_no_link():
    """Test that articles without links are skipped."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Article Without Link</title>
                <description>This has no link</description>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 0


def test_fetch_feed_multiple_articles():
    """Test fetching multiple articles."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Article 1</title>
                <link>https://example.com/1</link>
            </item>
            <item>
                <title>Article 2</title>
                <link>https://example.com/2</link>
            </item>
            <item>
                <title>Article 3</title>
                <link>https://example.com/3</link>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 3
    assert articles[0]['title'] == "Article 1"
    assert articles[1]['title'] == "Article 2"
    assert articles[2]['title'] == "Article 3"


def test_fetch_feed_network_error():
    """Test handling of network errors."""
    with patch('feedrr.fetcher.rss.requests.get', side_effect=Exception("Network error")):
        articles = fetch_feed("https://example.com/feed.xml")

    # Should return empty list on error
    assert articles == []


def test_fetch_feed_timeout():
    """Test timeout parameter is used."""
    mock_response = Mock()
    mock_response.content = b"<rss></rss>"
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response) as mock_get:
        fetch_feed("https://example.com/feed.xml", timeout=60)
        mock_get.assert_called_once_with("https://example.com/feed.xml", timeout=60)


def test_fetch_feed_untitled():
    """Test article without title gets 'Untitled'."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <link>https://example.com/article</link>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 1
    assert articles[0]['title'] == "Untitled"


def test_fetch_feed_image_from_media_content():
    """Test extracting image from media:content RSS tag."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
        <channel>
            <item>
                <title>Article with Media Content</title>
                <link>https://example.com/article</link>
                <media:content url="https://example.com/image.jpg" type="image/jpeg" />
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 1
    assert articles[0]['image_url'] == "https://example.com/image.jpg"


def test_fetch_feed_image_from_html_content():
    """Test extracting image from HTML content when no standard RSS image fields exist."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Article with Image in Content</title>
                <link>https://example.com/article</link>
                <description><![CDATA[
                    <p><img src="https://example.com/article-image.jpg" alt="Article image" /></p>
                    <p>This is the article content with an embedded image.</p>
                ]]></description>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 1
    assert articles[0]['image_url'] == "https://example.com/article-image.jpg"
    assert articles[0]['content'] is not None


def test_fetch_feed_image_from_content_field():
    """Test extracting image from content:encoded field (common in WordPress feeds)."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
        <channel>
            <item>
                <title>WordPress Article</title>
                <link>https://example.com/article</link>
                <content:encoded><![CDATA[
                    <a href="https://example.com/full-image.jpg">
                        <img class="alignleft" src="https://example.com/thumb-image.jpg" width="248" height="225" />
                    </a>
                    <p>Article content here...</p>
                ]]></content:encoded>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 1
    assert articles[0]['image_url'] == "https://example.com/thumb-image.jpg"


def test_fetch_feed_no_image():
    """Test article without any image sources returns None for image_url."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Article Without Image</title>
                <link>https://example.com/article</link>
                <description>Plain text description with no images</description>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 1
    assert articles[0]['image_url'] is None


def test_fetch_feed_image_priority():
    """Test that media:content takes priority over HTML content images."""
    mock_response = Mock()
    mock_response.content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
        <channel>
            <item>
                <title>Article with Multiple Image Sources</title>
                <link>https://example.com/article</link>
                <media:content url="https://example.com/priority-image.jpg" type="image/jpeg" />
                <description><![CDATA[
                    <img src="https://example.com/html-image.jpg" alt="HTML image" />
                ]]></description>
            </item>
        </channel>
    </rss>""".encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch('feedrr.fetcher.rss.requests.get', return_value=mock_response):
        articles = fetch_feed("https://example.com/feed.xml")

    assert len(articles) == 1
    # Should use media:content image, not HTML content image
    assert articles[0]['image_url'] == "https://example.com/priority-image.jpg"
