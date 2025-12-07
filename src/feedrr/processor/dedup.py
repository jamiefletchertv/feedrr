"""Content deduplication using embeddings."""

from typing import List, Optional
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from ..storage.models import Article


def serialize_embedding(embedding: np.ndarray) -> bytes:
    """Serialize numpy array to bytes for database storage."""
    return pickle.dumps(embedding)


def deserialize_embedding(embedding_bytes: bytes) -> np.ndarray:
    """Deserialize bytes back to numpy array."""
    return pickle.loads(embedding_bytes)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def generate_article_embedding(model: SentenceTransformer, article: Article) -> np.ndarray:
    """
    Generate embedding for an article based on title and content.

    Args:
        model: SentenceTransformer model
        article: Article object

    Returns:
        Numpy array embedding
    """
    # Combine title and content for embedding
    text = f"{article.title} {article.content or ''}"
    return model.encode(text)


def find_duplicate(
    model: SentenceTransformer,
    new_article: Article,
    existing_articles: List[Article],
    threshold: float = 0.85
) -> Optional[Article]:
    """
    Find if new article is a duplicate of any existing articles.

    Args:
        model: SentenceTransformer model
        new_article: Newly fetched article
        existing_articles: Articles from database to compare against
        threshold: Similarity threshold (0.85 = 85% similar)

    Returns:
        Original article if duplicate found, None otherwise
    """
    # Generate embedding for new article
    new_embedding = generate_article_embedding(model, new_article)

    # Compare with existing articles
    for existing in existing_articles:
        if not existing.embedding:
            continue  # Skip articles without embeddings

        try:
            existing_embedding = deserialize_embedding(existing.embedding)
            similarity = cosine_similarity(new_embedding, existing_embedding)

            if similarity >= threshold:
                return existing
        except Exception:
            # Skip if embedding deserialization fails
            continue

    return None


def mark_as_duplicate(article: Article, original: Article) -> None:
    """
    Mark an article as a duplicate of another.

    Args:
        article: Article to mark as duplicate
        original: Original article this is a duplicate of
    """
    article.is_duplicate = True
    article.duplicate_of_id = original.id
