from __future__ import annotations
from typing import Dict, List, Optional, Tuple

from todo_app.models import Project, Task, TaskStatus
from todo_app.repositories.project_repository import ProjectRepository
from todo_app.repositories.task_repository import TaskRepository

class InMemoryRepo(ProjectRepository, TaskRepository):
    def __init__(self) -> None:
        # Projects
        self._projects_by_id: Dict[str, Project] = {}
        self._project_name_index: Dict[str, str] = {}  # name -> project_id (enforce unique names)
        # Tasks
        self._tasks_by_id: Dict[str, Tuple[str, Task]] = {}  # task_id -> (project_id, Task)

    # -------- Projects --------
    def add_project(self, project: Project) -> None:
        if project.name in self._project_name_index:
            raise ValueError("Project name must be unique.")
        self._projects_by_id[project.id] = project
        self._project_name_index[project.name] = project.id

    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        return self._projects_by_id.get(project_id)

    def get_project_by_name(self, name: str) -> Optional[Project]:
        pid = self._project_name_index.get(name)
        return self._projects_by_id.get(pid) if pid else None

    def list_projects(self) -> List[Project]:
        # Sort by created_at ascending (as per requirement)
        return sorted(self._projects_by_id.values(), key=lambda p: p.created_at)

    def update_project(self, project: Project, *, new_name: Optional[str] = None,
                       new_description: Optional[str] = None) -> Project:
        if new_name is not None and new_name != project.name:
            if new_name in self._project_name_index:
                raise ValueError("Project name must be unique.")
            # Update name index
            old = project.name
            project.edit(name=new_name)
            del self._project_name_index[old]
            self._project_name_index[new_name] = project.id
        if new_description is not None:
            project.edit(description=new_description)
        return project

    def delete_project(self, project_id: str) -> bool:
        proj = self._projects_by_id.pop(project_id, None)
        if not proj:
            return False
        # remove name index
        self._project_name_index.pop(proj.name, None)
        # cascade delete tasks
        for t in list(proj.tasks):
            self.delete_task(t.id)  # removes from task map
        return True

    # -------- Tasks --------
    def add_task(self, project: Project, task: Task) -> None:
        project.add_task(task)
        self._tasks_by_id[task.id] = (project.id, task)

    def get_task(self, task_id: str) -> Optional[Task]:
        pair = self._tasks_by_id.get(task_id)
        return pair[1] if pair else None

    def list_tasks_of_project(self, project_id: str) -> List[Task]:
        proj = self._projects_by_id.get(project_id)
        return list(proj.tasks) if proj else []

    def update_task(self, task_id: str, **kwargs) -> Task:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("Task not found.")
        task.edit(
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            status=kwargs.get("status"),
            deadline_str=kwargs.get("deadline_str"),
        )
        return task

    def change_task_status(self, task_id: str, new_status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("Task not found.")
        task.change_status(new_status)
        return task

    def delete_task(self, task_id: str) -> bool:
        pair = self._tasks_by_id.pop(task_id, None)
        if not pair:
            return False
        project_id, task = pair
        proj = self._projects_by_id.get(project_id)
        if proj:
            proj.remove_task(task_id)
        return True
