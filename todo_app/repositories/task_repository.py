from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from todo_app.models import Project, Task


class TaskRepository(ABC):
    """Contract for task persistence operations."""

    @abstractmethod
    def add_task(self, project: Project, task: Task) -> None:
        """Attach a task to a project and persist it."""
        raise NotImplementedError

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def list_tasks_of_project(self, project_id: str) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task_id: str, **kwargs) -> Task:
        """Update fields of a task and return the updated one."""
        raise NotImplementedError

    @abstractmethod
    def change_task_status(self, task_id: str, new_status: str) -> Task:
        """Change status of a task."""
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        raise NotImplementedError
