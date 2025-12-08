from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_app.models import Project, Task
from todo_app.db.models import ProjectORM, TaskORM


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

# -------- Helper mappers --------

def _task_from_orm(orm: TaskORM) -> Task:
    status_str = orm.status.value if hasattr(orm.status, "value") else str(orm.status)
    t = Task(
        title=orm.title,
        description=orm.description or "",
        status=status_str,
        deadline=orm.deadline,
    )
    t.id = orm.id  # type: ignore[attr-defined]
    t.created_at = orm.created_at  # type: ignore[attr-defined]
    return t


class SqlAlchemyTaskRepository(TaskRepository):
    """SQLAlchemy-based implementation of TaskRepository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add_task(self, project: Project, task: Task) -> None:
        # Ensure the project exists in the database
        proj_orm = self._session.get(ProjectORM, project.id)  # type: ignore[attr-defined]
        if proj_orm is None:
            raise ValueError("Project not found in database.")

        orm = TaskORM(
            id=task.id,  # type: ignore[attr-defined]
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            project_id=proj_orm.id,
            created_at=task.created_at,  # type: ignore[attr-defined]
        )
        self._session.add(orm)
        self._session.commit()

    def get_task(self, task_id: str) -> Optional[Task]:
        orm = self._session.get(TaskORM, task_id)
        if orm is None:
            return None
        return _task_from_orm(orm)

    def list_tasks_of_project(self, project_id: str) -> List[Task]:
        stmt = select(TaskORM).where(TaskORM.project_id == project_id)
        orms = self._session.scalars(stmt).all()
        return [_task_from_orm(o) for o in orms]

    def update_task(self, task_id: str, **kwargs) -> Task:
        orm = self._session.get(TaskORM, task_id)
        if orm is None:
            raise ValueError("Task not found.")

        title = kwargs.get("title")
        description = kwargs.get("description")
        status = kwargs.get("status")
        deadline_str = kwargs.get("deadline_str")

        if title is not None:
            orm.title = title
        if description is not None:
            orm.description = description
        if status is not None:
            orm.status = status
        if deadline_str is not None:
            # You can use parse_deadline here again if desired
            from todo_app.models import parse_deadline  # local import to avoid circular dependency
            orm.deadline = parse_deadline(deadline_str)

        self._session.commit()
        self._session.refresh(orm)
        return _task_from_orm(orm)

    def change_task_status(self, task_id: str, new_status: str) -> Task:
        orm = self._session.get(TaskORM, task_id)
        if orm is None:
            raise ValueError("Task not found.")
        orm.status = new_status
        self._session.commit()
        self._session.refresh(orm)
        return _task_from_orm(orm)

    def delete_task(self, task_id: str) -> bool:
        orm = self._session.get(TaskORM, task_id)
        if orm is None:
            return False
        self._session.delete(orm)
        self._session.commit()
        return True
