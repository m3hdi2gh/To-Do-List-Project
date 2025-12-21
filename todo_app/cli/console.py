"""
Interactive CLI for ToDoList application.

.. deprecated::
    This CLI module is deprecated as of Phase 3.
    All functionality is now available through the FastAPI Web API.

    Migration guide:
        - Run API: uvicorn todo_app.api.main:app --reload
        - Swagger UI: http://localhost:8000/docs
        - ReDoc: http://localhost:8000/redoc

    The CLI will be removed in a future release.
"""

from __future__ import annotations

import sys
from typing import Optional, cast
from todo_app.models import TaskStatus
from todo_app.services import ProjectService, TaskService
from todo_app.repositories import (
    SqlAlchemyProjectRepository,
    SqlAlchemyTaskRepository,
)
from todo_app.db.session import SessionLocal


# ---------- Helpers (generic I/O) ----------

def prompt(msg: str) -> str:
    """Read a line from stdin and strip whitespace."""
    return input(msg).strip()


def confirm(msg: str = "Are you sure? (Y/n): ") -> bool:
    """Simple yes/no confirmation; default is yes."""
    ans = prompt(msg).lower()
    return ans in ("y", "yes", "")


# ---------- Helpers (domain-oriented) ----------

def choose_project(ps: ProjectService) -> Optional[str]:
    """Let the user choose a project and return its id."""
    projects = ps.list_projects()
    if not projects:
        print("No projects found.")
        return None

    print("\nProjects:")
    for idx, p in enumerate(projects, start=1):
        print(f"{idx}. {p.name} ({p.id})")

    while True:
        raw = prompt("Choose project number (or 'b' to go back): ")
        if raw.lower() == "b":
            return None
        try:
            n = int(raw)
            if 1 <= n <= len(projects):
                return projects[n - 1].id
            print("Out of range. Try again.")
        except ValueError:
            print("Invalid number. Try again.")


def choose_task(ts: TaskService, project_id: str) -> Optional[str]:
    """Let the user choose a task of a project and return its id."""
    tasks = ts.list_tasks_of_project(project_id)
    if not tasks:
        print("No tasks in this project.")
        return None

    print("\nTasks:")
    for idx, t in enumerate(tasks, start=1):
        print(f"{idx}. {t.title} ({t.id}) [{t.status}] deadline={t.deadline}")

    while True:
        raw = prompt("Choose task number (or 'b' to go back): ")
        if raw.lower() == "b":
            return None
        try:
            n = int(raw)
            if 1 <= n <= len(tasks):
                return tasks[n - 1].id
            print("Out of range. Try again.")
        except ValueError:
            print("Invalid number. Try again.")


def ask_status(default: TaskStatus = "todo") -> Optional[TaskStatus]:
    """
    Ask for a status; returns one of todo/ doing/done or None if user cancels.
    """
    while True:
        raw = prompt(f"Task status (todo/doing/done) [default {default}, 'b' to back]: ") or default
        if raw.lower() == "b":
            return None
        if raw in {"todo", "doing", "done"}:
            # Help the type checker: raw is guaranteed to be a valid TaskStatus here
            return cast(TaskStatus, raw)
        print("Invalid status. Allowed: todo/doing/done")


def ask_deadline() -> Optional[str]:
    """
    Ask for deadline string; returns None for blank.
    Service/entity will do strict validation (YYYY-MM-DD).
    """
    raw = prompt("Deadline (YYYY-MM-DD) [blank for none]: ")
    return raw or None


# ---------- Actions ----------

def action_create_project(ps: ProjectService) -> None:
    name = prompt("Project name: ")
    desc = prompt("Project description: ")
    try:
        p = ps.create_project(name=name, description=desc)
        print(f"Project created: {p.name} ({p.id})")
    except Exception as e:
        print(f"Error: {e}")


def action_edit_project(ps: ProjectService) -> None:
    pid = choose_project(ps)
    if not pid:
        return
    new_name = prompt("New name (blank to skip): ")
    new_desc = prompt("New description (blank to skip): ")
    try:
        p = ps.edit_project(pid, new_name=new_name or None, new_description=new_desc or None)
        print(f"Project updated: {p.name} ({p.id})")
    except Exception as e:
        print(f"Error: {e}")


def action_delete_project(ps: ProjectService) -> None:
    pid = choose_project(ps)
    if not pid:
        return
    if not confirm("Delete this project and cascade tasks? (Y/n): "):
        print("Cancelled.")
        return
    try:
        ps.delete_project(pid)
        print("Project deleted (cascaded tasks removed).")
    except Exception as e:
        print(f"Error: {e}")


def action_list_projects(ps: ProjectService) -> None:
    projects = ps.list_projects()
    if not projects:
        print("No projects available.")
        return
    print("\nProjects (sorted by creation time):")
    for p in projects:
        print(f"- {p.id} | {p.name} | {p.description} | tasks={len(p.tasks)}")


def action_add_task(ps: ProjectService, ts: TaskService) -> None:
    pid = choose_project(ps)
    if not pid:
        return
    title = prompt("Task title: ")
    desc = prompt("Task description: ")
    status = ask_status(default="todo")
    if status is None:  # user backed out
        print("Cancelled.")
        return
    deadline = ask_deadline()

    try:
        t = ts.add_task(project_id=pid, title=title, description=desc, status=status, deadline_str=deadline)
        print(f"Task created: {t.title} ({t.id})")
    except Exception as e:
        print(f"Error: {e}")


def action_edit_task(ps: ProjectService, ts: TaskService) -> None:
    pid = choose_project(ps)
    if not pid:
        return
    tid = choose_task(ts, pid)
    if not tid:
        return

    new_title = prompt("New title (blank to skip): ")
    new_desc = prompt("New description (blank to skip): ")
    raw_status = prompt("New status todo/doing/done (blank to skip): ").strip().lower()
    new_status = raw_status or None
    new_deadline = prompt("New deadline YYYY-MM-DD (blank to skip): ").strip() or None

    try:
        t2 = ts.edit_task(
            tid,
            title=(new_title or None),
            description=(new_desc or None),
            status=new_status,
            deadline_str=new_deadline,
        )
        print(f"Task updated: {t2.title} ({t2.id}) [{t2.status}] deadline={t2.deadline}")
    except Exception as e:
        print(f"Error: {e}")


def action_change_task_status(ps: ProjectService, ts: TaskService) -> None:
    pid = choose_project(ps)
    if not pid:
        return
    tid = choose_task(ts, pid)
    if not tid:
        return
    new_status = ask_status()
    if new_status is None:
        print("Cancelled.")
        return
    try:
        t2 = ts.change_status(tid, new_status)
        print(f"Status updated: {t2.title} -> {t2.status}")
    except Exception as e:
        print(f"Error: {e}")


def action_delete_task(ps: ProjectService, ts: TaskService) -> None:
    pid = choose_project(ps)
    if not pid:
        return
    tid = choose_task(ts, pid)
    if not tid:
        return
    if not confirm("Delete this task? (Y/n): "):
        print("Cancelled.")
        return
    try:
        ts.delete_task(tid)
        print("Task deleted.")
    except Exception as e:
        print(f"Error: {e}")


def action_list_tasks_of_project(ps: ProjectService, ts: TaskService) -> None:
    pid = choose_project(ps)
    if not pid:
        return
    tasks = ts.list_tasks_of_project(pid)
    if not tasks:
        print("No tasks in this project.")
        return
    print("\nTasks:")
    for t in tasks:
        print(f"- {t.id} | {t.title} | {t.status} | deadline={t.deadline}")


# ---------- Main Loop ----------

def run_cli() -> None:
    # === Deprecation Warning ===
    print("\n" + "=" * 60)
    print("⚠️  WARNING: CLI is deprecated!")
    print("=" * 60)
    print("This CLI interface will be removed in future versions.")
    print("Please use the new Web API instead:")
    print("  → Run: uvicorn todo_app.api.main:app --reload")
    print("  → Docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")
    # === End Deprecation Warning ===

    session = SessionLocal()

    project_repo = SqlAlchemyProjectRepository(session)
    task_repo = SqlAlchemyTaskRepository(session)

    ps = ProjectService(project_repo)
    ts = TaskService(project_repo=project_repo, task_repo=task_repo)

    MENU = """
==== To-Do CLI ====
1) Create project
2) Edit project
3) Delete project
4) List projects
5) Add task to project
6) Edit task
7) Change task status
8) Delete task
9) List tasks of a project
0) Exit
"""
    actions = {
        "1": lambda: action_create_project(ps),
        "2": lambda: action_edit_project(ps),
        "3": lambda: action_delete_project(ps),
        "4": lambda: action_list_projects(ps),
        "5": lambda: action_add_task(ps, ts),
        "6": lambda: action_edit_task(ps, ts),
        "7": lambda: action_change_task_status(ps, ts),
        "8": lambda: action_delete_task(ps, ts),
        "9": lambda: action_list_tasks_of_project(ps, ts),
    }

    try:
        while True:
            print(MENU)
            choice = prompt("Choose: ")
            if choice == "0":
                print("Bye!")
                sys.exit(0)

            action = actions.get(choice)
            if not action:
                print("Invalid option. Try again.")
                continue

            action()
    finally:
        session.close()