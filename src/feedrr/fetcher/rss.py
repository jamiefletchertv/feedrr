"""Simple RSS feed fetcher for MVP."""

import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from dateutil import parser as date_parser


def fetch_feed(feed_url: str, timeout: int = 30) -> List[Dict[str, Any]]:
    """
    Fetch and parse an RSS feed.

    Returns a list of article dictionaries with:
    - url: Article URL
    - title: Article title
    - content: Article content/summary
    - published_date: Publication date (datetime or None)

    Error Handling:
    - HTTP errors (404, 420 rate limits, etc.) are caught and logged
    - Network timeouts are caught and logged
    - Parse errors are caught and logged
    - Returns empty list on any error to allow other feeds to continue processing
    """
    articles = []

    try:
        # Fetch the feed
        response = requests.get(feed_url, timeout=timeout)
        response.raise_for_status()

        # Parse with feedparser
        feed = feedparser.parse(response.content)

        # Extract articles
        for entry in feed.entries:
            # Get URL (required)
            url = entry.get('link')
            if not url:
                continue

            # Get title (required)
            title = entry.get('title', 'Untitled')

            # Get content (try multiple fields)
            content = None
            if hasattr(entry, 'content'):
                content = entry.content[0].value
            elif hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description

            # Get published date
            published_date = None
            if hasattr(entry, 'published'):
                try:
                    published_date = date_parser.parse(entry.published)
                except:
                    pass
            elif hasattr(entry, 'updated'):
                try:
                    published_date = date_parser.parse(entry.updated)
                except:
                    pass

            # Get image URL (try multiple fields)
            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                # RSS media:content
                image_url = entry.media_content[0].get('url')
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                # RSS media:thumbnail
                image_url = entry.media_thumbnail[0].get('url')
            elif hasattr(entry, 'enclosures') and entry.enclosures:
                # RSS enclosure (check if it's an image)
                for enclosure in entry.enclosures:
                    if enclosure.get('type', '').startswith('image/'):
                        image_url = enclosure.get('href')
                        break
            elif hasattr(entry, 'links'):
                # Check links for image
                for link in entry.links:
                    if link.get('type', '').startswith('image/'):
                        image_url = link.get('href')
                        break

            articles.append({
                'url': url,
                'title': title,
                'content': content,
                'image_url': image_url,
                'published_date': published_date
            })

    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        return []

    return articles
