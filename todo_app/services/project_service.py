"""
ProjectService orchestrates project-level operations with business rules.
"""

from __future__ import annotations
from typing import List, Optional

from todo_app.config import settings
from todo_app.core import Project
from todo_app.storage import InMemoryRepo


class ProjectService:
    def __init__(self, repo: InMemoryRepo) -> None:
        self.repo = repo

    def create_project(self, *, name: str, description: str = "") -> Project:
        projects = self.repo.list_projects()
        if len(projects) >= settings.MAX_NUMBER_OF_PROJECT:
            raise ValueError(f"Project cap exceeded ({settings.MAX_NUMBER_OF_PROJECT}).")

        project = Project(name=name, description=description)
        self.repo.add_project(project)
        return project

    def edit_project(self, project_id: str, *, new_name: Optional[str] = None,
                     new_description: Optional[str] = None) -> Project:
        proj = self.repo.get_project_by_id(project_id)
        if not proj:
            raise ValueError("Project not found.")
        return self.repo.update_project(proj, new_name=new_name, new_description=new_description)

    def delete_project(self, project_id: str) -> None:
        ok = self.repo.delete_project(project_id)
        if not ok:
            raise ValueError("Project not found.")

    def list_projects(self) -> List[Project]:
        return self.repo.list_projects()

    def get_by_name(self, name: str) -> Optional[Project]:
        return self.repo.get_project_by_name(name)
