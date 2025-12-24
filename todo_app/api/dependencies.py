"""Dependency injection for FastAPI routes."""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from todo_app.db.session import SessionLocal
from todo_app.repositories import SqlAlchemyProjectRepository, SqlAlchemyTaskRepository
from todo_app.services import ProjectService, TaskService


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_db)]


def get_project_service(db: DBSession) -> ProjectService:
    """Create and return a ProjectService instance."""
    repo = SqlAlchemyProjectRepository(db)
    return ProjectService(repo)


def get_task_service(db: DBSession) -> TaskService:
    """Create and return a TaskService instance."""
    project_repo = SqlAlchemyProjectRepository(db)
    task_repo = SqlAlchemyTaskRepository(db)
    return TaskService(project_repo, task_repo)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]