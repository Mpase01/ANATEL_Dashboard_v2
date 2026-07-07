"""Database session helpers.

The project uses SQLAlchemy for PostgreSQL/Supabase access, but the database
connection is only created when a real DATABASE_URL is configured.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from app.core.config import Settings, get_settings

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session, sessionmaker
except ModuleNotFoundError:  # pragma: no cover - exercised only before deps install.
    create_engine = None
    Session = Any
    sessionmaker = None


def create_session_factory(settings: Settings | None = None):
    settings = settings or get_settings()
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not configured.")
    if create_engine is None or sessionmaker is None:
        raise RuntimeError("SQLAlchemy is not installed.")

    engine = create_engine(settings.database_url, pool_pre_ping=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def session_scope(settings: Settings | None = None) -> Iterator[Session]:
    session_factory = create_session_factory(settings)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
