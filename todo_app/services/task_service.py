from __future__ import annotations
from typing import List, Optional

from todo_app.config import settings
from todo_app.models import Task, parse_deadline
from todo_app.repositories.project_repository import ProjectRepository
from todo_app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository) -> None:
        self._project_repo = project_repo
        self._task_repo = task_repo

    def add_task(
            self,
            *,
            project_id: str,
            title: str,
            description: str = "",
            status: str = "todo",
            deadline_str: Optional[str] = None,
    ) -> Task:
        # Enforce cap over all tasks
        total_tasks = sum(len(p.tasks) for p in self._project_repo.list_projects())
        if total_tasks >= settings.MAX_NUMBER_OF_TASK:
            raise ValueError(f"Task cap exceeded ({settings.MAX_NUMBER_OF_TASK}).")

        proj = self._project_repo.get_project_by_id(project_id)
        if not proj:
            raise ValueError("Project not found.")

        task = Task(
            title=title,
            description=description,
            status=status,
            deadline=parse_deadline(deadline_str),
        )
        self._task_repo.add_task(proj, task)
        return task

    def change_status(self, task_id: str, new_status: str) -> Task:
        return self._task_repo.change_task_status(task_id, new_status)

    def edit_task(self, task_id: str, **kwargs) -> Task:
        return self._task_repo.update_task(task_id, **kwargs)

    def delete_task(self, task_id: str) -> None:
        ok = self._task_repo.delete_task(task_id)
        if not ok:
            raise ValueError("Task not found.")

    def list_tasks_of_project(self, project_id: str) -> List[Task]:
        return self._task_repo.list_tasks_of_project(project_id)
