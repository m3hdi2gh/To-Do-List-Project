"""
Task entity with basic validation and status changes.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date, UTC
from typing import Optional, Literal
from uuid import uuid4

TaskStatus = Literal["todo", "doing", "done"]
ALLOWED_STATUSES: set[str] = {"todo", "doing", "done"}


def parse_deadline(raw: Optional[str]) -> Optional[date]:
    """Parse YYYY-MM-DD into date; return None if raw is falsy."""
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")


def word_count(s: str) -> int:
    return len([w for w in s.split() if w.strip()])


@dataclass
class Task:
    title: str
    description: str = ""
    status: TaskStatus = "todo"
    deadline: Optional[date] = None
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        # Validate status
        if self.status not in ALLOWED_STATUSES:
            raise ValueError("Invalid status. Allowed: todo | doing | done")
        # Validate lengths (≤ 30 words title, ≤ 150 words description)
        if word_count(self.title) > 30:
            raise ValueError("Title must be ≤ 30 words.")
        if word_count(self.description) > 150:
            raise ValueError("Description must be ≤ 150 words.")

    def change_status(self, new_status: TaskStatus) -> None:
        """Change task status."""
        if new_status not in ALLOWED_STATUSES:
            raise ValueError("Invalid status. Allowed: todo | doing | done")
        self.status = new_status

    def edit(self, *, title: Optional[str] = None, description: Optional[str] = None,
             status: Optional[TaskStatus] = None, deadline_str: Optional[str] = None) -> None:
        """Edit task fields with validation."""
        if title is not None:
            if word_count(title) > 30:
                raise ValueError("Title must be ≤ 30 words.")
            self.title = title
        if description is not None:
            if word_count(description) > 150:
                raise ValueError("Description must be ≤ 150 words.")
            self.description = description
        if status is not None:
            self.change_status(status)
        if deadline_str is not None:
            self.deadline = parse_deadline(deadline_str)
