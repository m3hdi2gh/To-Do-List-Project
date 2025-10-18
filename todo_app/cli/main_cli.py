"""
Minimal CLI to interact with the To-Do app via services.
"""

from __future__ import annotations
import sys

from todo_app.services import ProjectService, TaskService
from todo_app.storage import InMemoryRepo


def prompt(msg: str) -> str:
    return input(msg).strip()


def choose_project_id(ps: ProjectService) -> str | None:
    projects = ps.list_projects()
    if not projects:
        print("No projects found.")
        return None
    print("\nProjects:")
    for idx, p in enumerate(projects, start=1):
        print(f"{idx}. {p.name} ({p.id})")
    raw = prompt("Choose project number: ")
    try:
        n = int(raw)
        return projects[n - 1].id
    except Exception:
        print("Invalid choice.")
        return None


def run_cli() -> None:
    repo = InMemoryRepo()
    ps = ProjectService(repo)
    ts = TaskService(repo)

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
    while True:
        print(MENU)
        choice = prompt("Choose: ")

        # Exit
        if choice == "0":
            sys.exit("Bye!")

        # Create Project
        elif choice == "1":
            name = prompt("Project name: ")
            desc = prompt("Project description: ")
            try:
                p = ps.create_project(name=name, description=desc)
                print(f"Project created: {p.name} ({p.id})")
            except Exception as e:
                print(f"Error: {e}")

        # Edit Project
        elif choice == "2":
            pid = choose_project_id(ps)
            if not pid:
                continue
            new_name = prompt("New name (blank to skip): ")
            new_desc = prompt("New description (blank to skip): ")
            try:
                p = ps.edit_project(pid,
                                    new_name=new_name or None,
                                    new_description=new_desc or None)
                print(f"Project updated: {p.name} ({p.id})")
            except Exception as e:
                print(f"Error: {e}")

        # Delete Project (cascade)
        elif choice == "3":
            pid = choose_project_id(ps)
            if not pid:
                continue
            try:
                ps.delete_project(pid)
                print("Project deleted (and related tasks cascaded).")
            except Exception as e:
                print(f"Error: {e}")

        # List Projects
        elif choice == "4":
            projects = ps.list_projects()
            if not projects:
                print("No projects available.")
            else:
                for p in projects:
                    print(f"- {p.id} | {p.name} | {p.description} | tasks={len(p.tasks)}")

        # Add Task
        elif choice == "5":
            pid = choose_project_id(ps)
            if not pid:
                continue
            title = prompt("Task title: ")
            desc = prompt("Task description: ")
            status = prompt("Task status (todo/doing/done) [default todo]: ") or "todo"
            deadline = prompt("Deadline (YYYY-MM-DD) [blank for none]: ") or None
            try:
                t = ts.add_task(project_id=pid, title=title, description=desc,
                                status=status, deadline_str=deadline)
                print(f"Task created: {t.title} ({t.id})")
            except Exception as e:
                print(f"Error: {e}")

        # Edit Task
        elif choice == "6":
            pid = choose_project_id(ps)
            if not pid:
                continue
            tasks = ts.list_tasks_of_project(pid)
            if not tasks:
                print("No tasks in this project.")
                continue
            for idx, t in enumerate(tasks, start=1):
                print(f"{idx}. {t.title} ({t.id}) [{t.status}] deadline={t.deadline}")
            raw = prompt("Choose task number: ")
            try:
                t = tasks[int(raw) - 1]
            except Exception:
                print("Invalid choice.")
                continue

            new_title = prompt("New title (blank to skip): ")
            new_desc = prompt("New description (blank to skip): ")
            new_status = prompt("New status todo/doing/done (blank to skip): ")
            new_deadline = prompt("New deadline YYYY-MM-DD (blank to skip): ")
            try:
                t2 = ts.edit_task(
                    t.id,
                    title=(new_title or None),
                    description=(new_desc or None),
                    status=(new_status or None),
                    deadline_str=(new_deadline or None),
                )
                print(f"Task updated: {t2.title} ({t2.id}) [{t2.status}]")
            except Exception as e:
                print(f"Error: {e}")

        # Change Task Status
        elif choice == "7":
            pid = choose_project_id(ps)
            if not pid:
                continue
            tasks = ts.list_tasks_of_project(pid)
            if not tasks:
                print("No tasks in this project.")
                continue
            for idx, t in enumerate(tasks, start=1):
                print(f"{idx}. {t.title} ({t.id}) [{t.status}]")
            raw = prompt("Choose task number: ")
            try:
                t = tasks[int(raw) - 1]
            except Exception:
                print("Invalid choice.")
                continue
            new_status = prompt("New status (todo/doing/done): ")
            try:
                t2 = ts.change_status(t.id, new_status)
                print(f"Status updated: {t2.title} -> {t2.status}")
            except Exception as e:
                print(f"Error: {e}")

        # Delete Task
        elif choice == "8":
            pid = choose_project_id(ps)
            if not pid:
                continue
            tasks = ts.list_tasks_of_project(pid)
            if not tasks:
                print("No tasks in this project.")
                continue
            for idx, t in enumerate(tasks, start=1):
                print(f"{idx}. {t.title} ({t.id})")
            raw = prompt("Choose task number: ")
            try:
                t = tasks[int(raw) - 1]
            except Exception:
                print("Invalid choice.")
                continue
            try:
                ts.delete_task(t.id)
                print("Task deleted.")
            except Exception as e:
                print(f"Error: {e}")

        # List Tasks of a Project
        elif choice == "9":
            pid = choose_project_id(ps)
            if not pid:
                continue
            tasks = ts.list_tasks_of_project(pid)
            if not tasks:
                print("No tasks in this project.")
            else:
                for t in tasks:
                    print(f"- {t.id} | {t.title} | {t.status} | deadline={t.deadline}")
        else:
            print("Invalid option. Try again.")
