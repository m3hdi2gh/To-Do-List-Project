"""
Project entity that contains a collection of tasks.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import List
from uuid import uuid4

from .task import Task, word_count


@dataclass
class Project:
    name: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        # Validate lengths (≤ 30 words name, ≤ 150 words description)
        if word_count(self.name) > 30:
            raise ValueError("Project name must be ≤ 30 words.")
        if word_count(self.description) > 150:
            raise ValueError("Project description must be ≤ 150 words.")

    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by id from the project; returns True if removed."""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < before

    def edit(self, *, name: str | None = None, description: str | None = None) -> None:
        """Edit project fields with validation."""
        if name is not None:
            if word_count(name) > 30:
                raise ValueError("Project name must be ≤ 30 words.")
            self.name = name
        if description is not None:
            if word_count(description) > 150:
                raise ValueError("Project description must be ≤ 150 words.")
            self.description = description
