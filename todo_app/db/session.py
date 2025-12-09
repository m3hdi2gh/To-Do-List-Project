from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo_app.config import settings


# SQLAlchemy Engine: manages connections to the Postgres database
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,   # For debugging, you can temporarily set to True to log SQL queries
    future=True,  # Use modern SQLAlchemy 2.x API
)


# Session factory: we use this wherever we need a database Session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
