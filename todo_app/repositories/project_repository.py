from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_app.models import Project, Task, TaskStatus
from todo_app.db.models import ProjectORM


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


# -------- Helper mappers --------


def _project_from_orm(orm: ProjectORM) -> Project:
    """
    Map ProjectORM -> domain Project (along with the list of Tasks).

    It is assumed that Project in todo_app.models has fields like:
      id, name, description, created_at, tasks
    and Task also has fields id, title, description, status, deadline, created_at.
    """
    # Initialize with keyword arguments to avoid issues with field order
    proj = Project(
        id=orm.id,
        name=orm.name,
        description=orm.description or "",
        created_at=orm.created_at,
    )

    # If Project by default creates its own list of tasks,
    # we just populate it here.
    # If desired, you can call proj.tasks.clear() beforehand.
    for torm in orm.tasks:
        status_str = cast(
            TaskStatus,
            torm.status.value if hasattr(torm.status, "value") else str(torm.status),
        )

        task = Task(
            id=torm.id,
            title=torm.title,
            description=torm.description or "",
            status=status_str,
            deadline=torm.deadline,
            created_at=torm.created_at,
        )
        proj.tasks.append(task)  # type: ignore[attr-defined]

    return proj


# -------- SQLAlchemy implementation --------


class SqlAlchemyProjectRepository(ProjectRepository):
    """SQLAlchemy-based implementation of ProjectRepository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add_project(self, project: Project) -> None:
        """
        Use the id and created_at of the Project (domain)
        to keep CLI behavior consistent as before.
        """
        orm = ProjectORM(
            id=project.id,        # type: ignore[attr-defined]
            name=project.name,
            description=project.description,
            created_at=project.created_at,  # type: ignore[attr-defined]
        )
        self._session.add(orm)
        self._session.commit()

    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        orm = self._session.get(ProjectORM, project_id)
        if orm is None:
            return None
        return _project_from_orm(orm)

    def get_project_by_name(self, name: str) -> Optional[Project]:
        stmt = select(ProjectORM).where(ProjectORM.name == name)
        orm = self._session.scalar(stmt)
        if orm is None:
            return None
        return _project_from_orm(orm)

    def list_projects(self) -> List[Project]:
        stmt = select(ProjectORM).order_by(ProjectORM.created_at.asc())
        orms = self._session.scalars(stmt).all()
        return [_project_from_orm(o) for o in orms]

    def update_project(
        self,
        project: Project,
        *,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Project:
        orm = self._session.get(ProjectORM, project.id)  # type: ignore[attr-defined]
        if orm is None:
            raise ValueError("Project not found.")

        if new_name is not None:
            orm.name = new_name
        if new_description is not None:
            orm.description = new_description

        self._session.commit()
        self._session.refresh(orm)
        return _project_from_orm(orm)

    def delete_project(self, project_id: str) -> bool:
        orm = self._session.get(ProjectORM, project_id)
        if orm is None:
            return False
        self._session.delete(orm)
        self._session.commit()
        return True
