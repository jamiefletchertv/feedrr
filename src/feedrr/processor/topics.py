"""Simple topic tagging using keyword similarity."""

from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np


# Global model instance (lazy loaded)
_model = None


def get_model() -> SentenceTransformer:
    """Get or load the sentence transformer model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _model


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def assign_topics(article_text: str, topic_definitions: List[Dict]) -> List[str]:
    """
    Assign topics to an article based on keyword similarity.

    Args:
        article_text: Article title + content
        topic_definitions: List of dicts with 'name', 'slug', 'keywords'

    Returns:
        List of topic slugs that match
    """
    if not article_text or not article_text.strip():
        return ['general']  # Default topic

    model = get_model()

    # Generate embedding for article
    article_embedding = model.encode(article_text)

    # Calculate similarity for each topic
    matches = []
    for topic in topic_definitions:
        # Combine keywords into text
        keywords_text = ' '.join(topic.get('keywords', []))
        if not keywords_text:
            continue

        # Generate embedding for keywords
        keywords_embedding = model.encode(keywords_text)

        # Calculate similarity
        similarity = cosine_similarity(article_embedding, keywords_embedding)

        # Threshold for matching
        if similarity > 0.3:  # Simple threshold
            matches.append((topic['slug'], similarity))

    # Sort by similarity and return top matches
    matches.sort(key=lambda x: x[1], reverse=True)

    # Return top 2 topics, or 'general' if no matches
    if matches:
        return [slug for slug, _ in matches[:2]]
    else:
        return ['general']
