from __future__ import annotations

from datetime import datetime, date, UTC
from typing import Optional, List

import enum
from sqlalchemy import (
    String,
    Text,
    Date,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from todo_app.db.base import Base


class TaskStatusEnum(str, enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class ProjectORM(Base):
    __tablename__ = "projects"

    # PK should be simple and integer (for DB)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Project name must be unique (as per doc)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Description can be empty
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # One-to-many relationship with Task
    tasks: Mapped[List["TaskORM"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # FK to project
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[TaskStatusEnum] = mapped_column(
        Enum(TaskStatusEnum),
        default=TaskStatusEnum.TODO,
        nullable=False,
    )

    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    closed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Reverse relationship: each task is connected to a project
    project: Mapped["ProjectORM"] = relationship(
        back_populates="tasks",
    )
