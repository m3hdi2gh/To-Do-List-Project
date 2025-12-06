from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from todo_app.models import Project


class ProjectRepository(ABC):
    """Contract for project persistence operations."""

    @abstractmethod
    def add_project(self, project: Project) -> None:
        """Add a new project. Must enforce unique project.name."""
        raise NotImplementedError

    @abstractmethod
    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        raise NotImplementedError

    @abstractmethod
    def get_project_by_name(self, name: str) -> Optional[Project]:
        raise NotImplementedError

    @abstractmethod
    def list_projects(self) -> List[Project]:
        """Return projects sorted by created_at ascending (as in Phase 1)."""
        raise NotImplementedError

    @abstractmethod
    def update_project(
        self,
        project: Project,
        *,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Project:
        """Update project fields and return the updated instance."""
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """Delete project (and cascade-related tasks if needed)."""
        raise NotImplementedError
