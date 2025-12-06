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

            articles.append({
                'url': url,
                'title': title,
                'content': content,
                'published_date': published_date
            })

    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        return []

    return articles
