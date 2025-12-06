"""Simple database models for feedrr MVP."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, Session

Base = declarative_base()


class Source(Base):
    """RSS feed source."""

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    feed_url = Column(String(500), unique=True, nullable=False)
    website_url = Column(String(500))
    enabled = Column(Boolean, default=True)
    last_fetched = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    articles = relationship("Article", back_populates="source")

    def __repr__(self) -> str:
        return f"<Source(name='{self.name}', enabled={self.enabled})>"


class Article(Base):
    """Article from RSS feed."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    url = Column(String(1000), unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    published_date = Column(DateTime)
    fetched_date = Column(DateTime, default=datetime.utcnow)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)

    # Relationship
    source = relationship("Source", back_populates="articles")

    def __repr__(self) -> str:
        return f"<Article(title='{self.title[:50]}...')>"


def create_database(db_path: str) -> None:
    """Create database tables."""
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)


def get_session(db_path: str) -> Session:
    """Get database session."""
    engine = create_engine(f"sqlite:///{db_path}")
    return Session(engine)
