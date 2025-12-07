"""Tests for content deduplication."""

import pytest
import numpy as np
from unittest.mock import Mock, MagicMock
from sentence_transformers import SentenceTransformer

from feedrr.processor.dedup import (
    serialize_embedding,
    deserialize_embedding,
    cosine_similarity,
    generate_article_embedding,
    find_duplicate,
    mark_as_duplicate,
)
from feedrr.storage.models import Article, Source


def test_serialize_deserialize_embedding():
    """Test embedding serialization and deserialization."""
    # Create a sample embedding
    original = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

    # Serialize
    serialized = serialize_embedding(original)
    assert isinstance(serialized, bytes)

    # Deserialize
    deserialized = deserialize_embedding(serialized)
    assert isinstance(deserialized, np.ndarray)
    np.testing.assert_array_equal(original, deserialized)


def test_cosine_similarity_identical():
    """Test cosine similarity with identical vectors."""
    vec = np.array([1.0, 2.0, 3.0])
    similarity = cosine_similarity(vec, vec)
    assert abs(similarity - 1.0) < 0.0001  # Should be 1.0 (identical)


def test_cosine_similarity_orthogonal():
    """Test cosine similarity with orthogonal vectors."""
    vec1 = np.array([1.0, 0.0, 0.0])
    vec2 = np.array([0.0, 1.0, 0.0])
    similarity = cosine_similarity(vec1, vec2)
    assert abs(similarity - 0.0) < 0.0001  # Should be 0.0 (orthogonal)


def test_cosine_similarity_opposite():
    """Test cosine similarity with opposite vectors."""
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = np.array([-1.0, -2.0, -3.0])
    similarity = cosine_similarity(vec1, vec2)
    assert abs(similarity - (-1.0)) < 0.0001  # Should be -1.0 (opposite)


def test_cosine_similarity_similar():
    """Test cosine similarity with similar vectors."""
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = np.array([1.1, 2.1, 2.9])
    similarity = cosine_similarity(vec1, vec2)
    assert similarity > 0.99  # Should be very similar


def test_generate_article_embedding():
    """Test generating embedding for an article."""
    # Mock model
    mock_model = Mock(spec=SentenceTransformer)
    mock_embedding = np.array([0.1, 0.2, 0.3])
    mock_model.encode.return_value = mock_embedding

    # Create mock article
    article = Mock(spec=Article)
    article.title = "Test Article"
    article.content = "This is test content"

    # Generate embedding
    embedding = generate_article_embedding(mock_model, article)

    # Verify
    mock_model.encode.assert_called_once_with("Test Article This is test content")
    np.testing.assert_array_equal(embedding, mock_embedding)


def test_generate_article_embedding_no_content():
    """Test generating embedding for article without content."""
    mock_model = Mock(spec=SentenceTransformer)
    mock_embedding = np.array([0.1, 0.2, 0.3])
    mock_model.encode.return_value = mock_embedding

    article = Mock(spec=Article)
    article.title = "Test Article"
    article.content = None

    embedding = generate_article_embedding(mock_model, article)

    mock_model.encode.assert_called_once_with("Test Article ")
    np.testing.assert_array_equal(embedding, mock_embedding)


def test_find_duplicate_exact_match():
    """Test finding duplicate with exact match."""
    # Mock model
    mock_model = Mock(spec=SentenceTransformer)
    identical_embedding = np.array([0.5, 0.5, 0.5])
    mock_model.encode.return_value = identical_embedding

    # New article
    new_article = Mock(spec=Article)
    new_article.title = "Breaking News"
    new_article.content = "Important story"

    # Existing article with same embedding
    existing = Mock(spec=Article)
    existing.id = 1
    existing.embedding = serialize_embedding(identical_embedding)

    # Find duplicate
    duplicate = find_duplicate(mock_model, new_article, [existing])

    assert duplicate == existing


def test_find_duplicate_similar_content():
    """Test finding duplicate with similar content (above threshold)."""
    mock_model = Mock(spec=SentenceTransformer)

    # New article embedding
    new_embedding = np.array([1.0, 0.0, 0.0])
    mock_model.encode.return_value = new_embedding

    new_article = Mock(spec=Article)
    new_article.title = "Test Article"
    new_article.content = "Test content"

    # Existing article with very similar embedding (90% similar)
    similar_embedding = np.array([0.9, 0.1, 0.0])
    existing = Mock(spec=Article)
    existing.id = 1
    existing.embedding = serialize_embedding(similar_embedding)

    duplicate = find_duplicate(mock_model, new_article, [existing], threshold=0.85)

    assert duplicate == existing


def test_find_duplicate_below_threshold():
    """Test that articles below similarity threshold are not marked as duplicates."""
    mock_model = Mock(spec=SentenceTransformer)

    # New article embedding
    new_embedding = np.array([1.0, 0.0, 0.0])
    mock_model.encode.return_value = new_embedding

    new_article = Mock(spec=Article)
    new_article.title = "Different Article"
    new_article.content = "Different content"

    # Existing article with different embedding (50% similar)
    different_embedding = np.array([0.5, 0.5, 0.5])
    existing = Mock(spec=Article)
    existing.id = 1
    existing.embedding = serialize_embedding(different_embedding)

    duplicate = find_duplicate(mock_model, new_article, [existing], threshold=0.85)

    assert duplicate is None


def test_find_duplicate_no_existing_articles():
    """Test finding duplicate when no existing articles."""
    mock_model = Mock(spec=SentenceTransformer)
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])

    new_article = Mock(spec=Article)
    new_article.title = "New Article"
    new_article.content = "Fresh content"

    duplicate = find_duplicate(mock_model, new_article, [])

    assert duplicate is None


def test_find_duplicate_no_embeddings():
    """Test finding duplicate when existing articles have no embeddings."""
    mock_model = Mock(spec=SentenceTransformer)
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])

    new_article = Mock(spec=Article)
    new_article.title = "New Article"
    new_article.content = "Fresh content"

    # Existing article without embedding
    existing = Mock(spec=Article)
    existing.id = 1
    existing.embedding = None

    duplicate = find_duplicate(mock_model, new_article, [existing])

    assert duplicate is None


def test_find_duplicate_multiple_existing():
    """Test finding duplicate among multiple existing articles."""
    mock_model = Mock(spec=SentenceTransformer)

    new_embedding = np.array([1.0, 0.0, 0.0])
    mock_model.encode.return_value = new_embedding

    # First existing - not similar
    existing1 = Mock(spec=Article)
    existing1.id = 1
    existing1.embedding = serialize_embedding(np.array([0.0, 1.0, 0.0]))

    # Second existing - very similar (duplicate)
    existing2 = Mock(spec=Article)
    existing2.id = 2
    existing2.embedding = serialize_embedding(np.array([0.95, 0.05, 0.0]))

    # Third existing - not similar
    existing3 = Mock(spec=Article)
    existing3.id = 3
    existing3.embedding = serialize_embedding(np.array([0.0, 0.0, 1.0]))

    duplicate = find_duplicate(
        mock_model,
        new_article := Mock(spec=Article),
        [existing1, existing2, existing3],
        threshold=0.85
    )

    # Should find the second article as duplicate
    assert duplicate == existing2


def test_find_duplicate_corrupted_embedding():
    """Test that corrupted embeddings are skipped gracefully."""
    mock_model = Mock(spec=SentenceTransformer)
    mock_model.encode.return_value = np.array([1.0, 0.0, 0.0])

    new_article = Mock(spec=Article)
    new_article.title = "New Article"
    new_article.content = "Content"

    # Article with corrupted embedding
    existing = Mock(spec=Article)
    existing.id = 1
    existing.embedding = b"corrupted data"

    # Should not crash, should return None
    duplicate = find_duplicate(mock_model, new_article, [existing])
    assert duplicate is None


def test_mark_as_duplicate():
    """Test marking an article as duplicate."""
    article = Mock(spec=Article)
    article.is_duplicate = False
    article.duplicate_of_id = None

    original = Mock(spec=Article)
    original.id = 42

    mark_as_duplicate(article, original)

    assert article.is_duplicate is True
    assert article.duplicate_of_id == 42


def test_mark_as_duplicate_already_marked():
    """Test marking an already-duplicate article."""
    article = Mock(spec=Article)
    article.is_duplicate = True
    article.duplicate_of_id = 10

    original = Mock(spec=Article)
    original.id = 42

    mark_as_duplicate(article, original)

    # Should update to new original
    assert article.is_duplicate is True
    assert article.duplicate_of_id == 42


def test_integration_duplicate_workflow():
    """Integration test for complete duplicate detection workflow."""
    # Create mock model with realistic behavior
    mock_model = Mock(spec=SentenceTransformer)

    # Simulate two similar articles about the same story
    article1_embedding = np.array([0.8, 0.2, 0.1, 0.05])
    article2_embedding = np.array([0.82, 0.18, 0.12, 0.04])  # Very similar

    # First article (original)
    article1 = Mock(spec=Article)
    article1.id = 1
    article1.title = "Netflix acquires Warner Bros"
    article1.content = "Netflix has struck a deal to acquire Warner Bros..."
    article1.embedding = serialize_embedding(article1_embedding)
    article1.is_duplicate = False

    # Second article (duplicate from different source)
    article2 = Mock(spec=Article)
    article2.id = 2
    article2.title = "Netflix seals Warner Bros deal"
    article2.content = "In a major acquisition, Netflix has acquired Warner Bros..."
    article2.is_duplicate = False
    article2.duplicate_of_id = None

    # Simulate encoding the second article
    mock_model.encode.return_value = article2_embedding

    # Find if article2 is duplicate of article1
    duplicate_of = find_duplicate(mock_model, article2, [article1], threshold=0.85)

    # Should find article1 as the original
    assert duplicate_of == article1

    # Mark article2 as duplicate
    mark_as_duplicate(article2, duplicate_of)

    assert article2.is_duplicate is True
    assert article2.duplicate_of_id == 1
