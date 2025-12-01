from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Shared SQLAlchemy Declarative Base for all ORM models.

    Later, all ORM model classes will inherit from this Base.
    """

    # Optional: automatically generate table name = lowercase class name
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()
