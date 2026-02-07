"""Database engine and session configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# Create engine with behavior depending on DB dialect. SQLite requires
# `connect_args={"check_same_thread": False}` when used with the standard
# (synchronous) SQLAlchemy session in multi-threaded environments like
# FastAPI's default server threads.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # Enable automatic reconnection
        pool_size=10,  # Set connection pool size
        max_overflow=20,  # Maximum number of connections that can be created beyond pool_size
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Provide a database session for request handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
