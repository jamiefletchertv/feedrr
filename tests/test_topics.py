"""Tests for topic tagging processor."""

import pytest
from unittest.mock import Mock, patch
import numpy as np

from feedrr.processor.topics import assign_topics, cosine_similarity


def test_cosine_similarity():
    """Test cosine similarity calculation."""
    # Identical vectors should have similarity 1.0
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([1.0, 0.0, 0.0])
    assert abs(cosine_similarity(a, b) - 1.0) < 0.001

    # Orthogonal vectors should have similarity 0.0
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert abs(cosine_similarity(a, b) - 0.0) < 0.001


def test_assign_topics_empty_article():
    """Test that empty articles get 'general' topic."""
    topics = [
        {"name": "Tech", "slug": "tech", "keywords": ["software", "code"]},
    ]

    # Empty text
    result = assign_topics("", topics)
    assert result == ["general"]

    # Whitespace only
    result = assign_topics("   ", topics)
    assert result == ["general"]


def test_assign_topics_no_match():
    """Test articles with no topic matches get 'general'."""
    topics = [
        {"name": "Tech", "slug": "tech", "keywords": ["software", "programming"]},
    ]

    # Mock the model to return low similarity
    with patch('feedrr.processor.topics.get_model') as mock_get_model:
        mock_model = Mock()
        mock_model.encode.return_value = np.array([0.1, 0.1, 0.1])
        mock_get_model.return_value = mock_model

        # Override cosine_similarity to return low value
        with patch('feedrr.processor.topics.cosine_similarity', return_value=0.2):
            result = assign_topics("cats and dogs and animals", topics)
            assert result == ["general"]


def test_assign_topics_single_match():
    """Test article matching a single topic."""
    topics = [
        {"name": "Tech", "slug": "tech", "keywords": ["software", "programming", "code"]},
        {"name": "Science", "slug": "science", "keywords": ["research", "study", "experiment"]},
    ]

    # Mock the model
    with patch('feedrr.processor.topics.get_model') as mock_get_model:
        mock_model = Mock()

        # Create different embeddings for article and topics
        article_embedding = np.array([1.0, 0.0, 0.0])
        tech_embedding = np.array([0.9, 0.1, 0.0])  # High similarity
        science_embedding = np.array([0.0, 1.0, 0.0])  # Low similarity

        def encode_side_effect(text):
            if "programming" in text or "software" in text:
                return tech_embedding
            elif "research" in text or "study" in text:
                return science_embedding
            else:
                return article_embedding

        mock_model.encode.side_effect = encode_side_effect
        mock_get_model.return_value = mock_model

        result = assign_topics("New programming language released", topics)

        # Should match tech topic
        assert "tech" in result
        assert "science" not in result


def test_assign_topics_multiple_matches():
    """Test article matching multiple topics."""
    topics = [
        {"name": "Tech", "slug": "tech", "keywords": ["software", "ai", "programming"]},
        {"name": "Business", "slug": "business", "keywords": ["startup", "company", "market"]},
        {"name": "Science", "slug": "science", "keywords": ["research", "study"]},
    ]

    # Mock to return high similarity for two topics
    with patch('feedrr.processor.topics.get_model') as mock_get_model:
        mock_model = Mock()
        mock_model.encode.return_value = np.array([1.0, 1.0, 1.0])
        mock_get_model.return_value = mock_model

        # Mock cosine_similarity to return different values
        similarity_values = [0.6, 0.5, 0.2]  # tech, business, science
        with patch('feedrr.processor.topics.cosine_similarity', side_effect=similarity_values):
            result = assign_topics("AI startup launches new product", topics)

            # Should return top 2 matches
            assert len(result) == 2
            assert "tech" in result
            assert "business" in result
            assert "science" not in result


def test_assign_topics_no_keywords():
    """Test topic with no keywords is skipped."""
    topics = [
        {"name": "Tech", "slug": "tech", "keywords": []},  # No keywords
        {"name": "Business", "slug": "business", "keywords": ["startup", "company"]},
    ]

    with patch('feedrr.processor.topics.get_model') as mock_get_model:
        mock_model = Mock()
        mock_model.encode.return_value = np.array([1.0, 1.0, 1.0])
        mock_get_model.return_value = mock_model

        with patch('feedrr.processor.topics.cosine_similarity', return_value=0.5):
            result = assign_topics("New startup founded", topics)

            # Should only match business, not tech
            assert "business" in result
            assert "tech" not in result


def test_assign_topics_sorting():
    """Test that topics are sorted by similarity."""
    topics = [
        {"name": "Tech", "slug": "tech", "keywords": ["software"]},
        {"name": "Business", "slug": "business", "keywords": ["startup"]},
        {"name": "Science", "slug": "science", "keywords": ["research"]},
    ]

    with patch('feedrr.processor.topics.get_model') as mock_get_model:
        mock_model = Mock()
        mock_model.encode.return_value = np.array([1.0, 1.0, 1.0])
        mock_get_model.return_value = mock_model

        # Return similarities in non-sorted order: tech=0.4, business=0.7, science=0.5
        similarity_values = [0.4, 0.7, 0.5]
        with patch('feedrr.processor.topics.cosine_similarity', side_effect=similarity_values):
            result = assign_topics("Test article", topics)

            # Should return top 2, sorted by similarity: business (0.7), science (0.5)
            assert len(result) == 2
            assert result[0] == "business"
            assert result[1] == "science"
