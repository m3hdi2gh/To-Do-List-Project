# 📝 To-Do List App (Python OOP — Postgres & SQLAlchemy)

A command-line **To-Do List application** built with:

- **Clean Python OOP domain models** (`Project`, `Task`)
- **Repository pattern** (in-memory + SQLAlchemy)
- **PostgreSQL** for persistence
- **Alembic** for database migrations
- A simple **scheduler** to auto-close overdue tasks

This project is developed incrementally in two phases:

- **Phase 1** → Pure CLI + in-memory storage  
- **Phase 2 (current)** → Proper persistence layer with PostgreSQL, SQLAlchemy ORM, Alembic, and background scheduling.

---

## 🚀 Main Features

### 🧩 Project Management
- Create new projects with name and description  
- Edit project details  
- Delete projects (with cascade deletion of tasks)  
- List all existing projects (sorted by creation time)

### ✅ Task Management
- Add tasks to a specific project  
- Edit task fields (title, description, status, deadline)  
- Change task status (`todo`, `doing`, `done`)  
- Delete tasks  
- List all tasks of a selected project  

### ⚙️ Configuration & Limits
- Environment-driven configuration via `.env` / OS env vars:
  - `MAX_NUMBER_OF_PROJECT` (default: 10)
  - `MAX_NUMBER_OF_TASK` (default: 100)
  - Database connection values (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`)
- Validation on text length (titles/descriptions) and task status
- Clear error messages in the CLI

### 🗄️ Persistence & Migrations (Phase 2)
- **PostgreSQL** as the main data store (via `docker-compose`)
- **SQLAlchemy ORM** models:
  - `ProjectORM` ↔ domain `Project`
  - `TaskORM` ↔ domain `Task`
- **Alembic**:
  - Tracks schema in `alembic/versions/…`
  - Initial migration creates `projects` and `tasks` tables
- IDs are stored as `UUID` **strings** (length 36) in DB to match domain IDs.

### ⏱️ Auto-Close Overdue Tasks (Phase 2)
- Management command:
  - `poetry run python -m todo_app.commands.autoclose_overdue`
- Logic:
  - Finds tasks with `deadline < today` and `status != "done"`
  - Sets `status = "done"` and updates `closed_at` to the current time
- Result:
  - Keeps old overdue tasks from staying in “todo/doing” forever.

### 🕒 Simple Scheduler (Phase 2)
- Separate command:
  - `poetry run python -m todo_app.commands.scheduler`
- Uses the `schedule` library
- In development mode, runs the auto-close job **every 15 seconds**:
  - Useful for demo/testing during presentation
- Can be later adjusted to run every minute/hour/day in a real deployment.

---

## 🧠 Architecture Overview

### Domain Layer (`todo_app/models`)
- **`Project`**
  - Fields: `id`, `name`, `description`, `created_at`, `tasks`
  - Validation: max word count for name/description
  - Methods: `add_task`, `remove_task`, `edit`
- **`Task`**
  - Fields: `id`, `title`, `description`, `status`, `deadline`, `created_at`
  - Validation: status must be one of `todo | doing | done`, word limits
  - Methods: `change_status`, `edit`
- **Helpers**
  - `parse_deadline(raw: str | None) -> date | None`

### Persistence Layer

#### ORM Models (`todo_app/db/models.py`)
- `ProjectORM`  
  - `id: String(36)` (UUID string, PK)  
  - `name: String(100)` (unique, not null)  
  - `description: Text`  
  - `created_at: DateTime(timezone=True)`  
  - Relationship: `tasks` → list of `TaskORM` (cascade delete)

- `TaskORM`  
  - `id: String(36)` (UUID string, PK)  
  - `project_id: String(36)` (FK → `projects.id`, `ondelete="CASCADE"`)  
  - `title: String(200)`  
  - `description: Text`  
  - `status: Enum(TaskStatusEnum)` where values are `"todo" | "doing" | "done"`  
  - `deadline: Date | None`  
  - `created_at: DateTime(timezone=True)`  
  - `closed_at: DateTime(timezone=True) | None`  
  - Relationship: `project` → `ProjectORM`

- `TaskStatusEnum(str, enum.Enum)`  
  - Members: `TODO = "todo"`, `DOING = "doing"`, `DONE = "done"`

#### Repositories (`todo_app/repositories`)
- **Interfaces**
  - `ProjectRepository`
    - `add_project`, `get_project_by_id`, `get_project_by_name`,
      `list_projects`, `update_project`, `delete_project`
  - `TaskRepository`
    - `add_task`, `get_task`, `list_tasks_of_project`,
      `update_task`, `change_task_status`, `delete_task`

- **In-memory implementation**  
  - `InMemoryRepo(ProjectRepository, TaskRepository)`  
  - Uses Python dicts for IDs and name indexing  
  - Cascade deletes tasks when a project is removed  
  - Kept for potential tests / alternative runtime modes

- **SQLAlchemy implementations**
  - `SqlAlchemyProjectRepository(Session)`
    - Works with `ProjectORM`
    - Maps between domain `Project` and `ProjectORM` via `_project_from_orm`
  - `SqlAlchemyTaskRepository(Session)`
    - Works with `TaskORM`
    - Converts `status` to/from `TaskStatusEnum`
    - Maps between domain `Task` and `TaskORM` via `_task_from_orm`

### Services (`todo_app/services`)
- **ProjectService**
  - Depends on `ProjectRepository`
  - Enforces `MAX_NUMBER_OF_PROJECT`
  - Provides methods to create/edit/delete/list projects

- **TaskService**
  - Depends on both `ProjectRepository` & `TaskRepository`
  - Enforces global `MAX_NUMBER_OF_TASK`
  - Validates project existence before adding tasks
  - Uses `parse_deadline` for deadline parsing
  - Provides methods to add/edit/delete/change status/list tasks

### CLI Layer (`todo_app/cli/console.py`)
- Uses **SQLAlchemy repositories** by default:
  - Creates `SessionLocal()`
  - Instantiates `SqlAlchemyProjectRepository` & `SqlAlchemyTaskRepository`
  - Injects them into `ProjectService` & `TaskService`
- Provides interactive menu with options 1–9 + exit
- Handles user input, calls services, and prints results.

---

## 🏗️ Updated Project Structure

```text
├── todo_app/
│   ├── cli/
│   │   ├── __init__.py        # Exposes run_cli
│   │   └── console.py         # Interactive CLI implementation
│   │
│   ├── commands/              # Management commands (Phase 2)
│   │   ├── __init__.py
│   │   ├── autoclose_overdue.py  # Auto-close overdue tasks once
│   │   └── scheduler.py          # Runs autoclose job periodically
│   │
│   ├── config/
│   │   ├── __init__.py        # Exposes Settings instance
│   │   └── settings.py        # Loads environment variables (.env)
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py            # SQLAlchemy Base
│   │   ├── models.py          # ProjectORM, TaskORM, TaskStatusEnum
│   │   └── session.py         # Engine + SessionLocal
│   │
│   ├── models/                # Domain entities (Phase 1 core)
│   │   ├── __init__.py        # Exports Project, Task, TaskStatus, parse_deadline
│   │   ├── project.py         # Project entity
│   │   └── task.py            # Task entity
│   │
│   ├── repositories/          # Repository interfaces & implementations
│   │   ├── __init__.py
│   │   ├── in_memory_repo.py           # In-memory Project+Task repo
│   │   ├── project_repository.py       # ProjectRepository + SQLAlchemy impl
│   │   └── task_repository.py          # TaskRepository + SQLAlchemy impl
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── project_service.py  # Project business logic
│   │   └── task_service.py     # Task business logic
│   │
│   ├── exceptions/
│   │   └── __init__.py         # (Reserved for custom exceptions)
│   │
│   └── __init__.py             # Root package docstring
│
├── alembic/
│   ├── README
│   ├── env.py                  # Alembic environment config
│   ├── script.py.mako          # Template for new migrations
│   └── versions/
│       └── e0372bb1cbb6_create_projects_and_tasks_tables.py
│
├── docker-compose.yml          # PostgreSQL service for development
├── alembic.ini                 # Alembic configuration
├── .env.example                # Example env vars for the project
├── .gitignore
├── pyproject.toml              # Poetry project & dependencies
├── README.md                   # This file
└── main.py                     # Entry point for CLI (run_cli)
````

---

## ⚙️ Environment & Configuration

### 1️⃣ Create `.env` file

Copy `.env.example`:

```bash
cp .env.example .env
```

Default values (matching `docker-compose.yml`):

```env
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=100

DB_HOST=localhost
DB_PORT=5432
DB_NAME=todolist
DB_USER=todolist_user
DB_PASSWORD=todolist_password
```

You can override these in `.env` without changing code.

---

## 📦 Installation (with Poetry)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/m3hdi2gh/To-Do-List-Project.git
cd To-Do-List-Project
```

### 2️⃣ Install dependencies

```bash
poetry install
```

---

## 🗄️ Run PostgreSQL (via Docker)

From project root:

```bash
docker compose up -d
```

This will start a `postgres:16` container with:

* DB: `todolist`
* User: `todolist_user`
* Password: `todolist_password`
* Port: `5432`

To stop and clean everything (container + volume):

```bash
docker compose down -v
```

---

## 🔁 Apply Database Migrations (Alembic)

After the DB is up, run:

```bash
poetry run alembic upgrade head
```

This will create the `projects` and `tasks` tables and the `alembic_version` table.

You can verify tables exist:

```bash
poetry run python -c "from sqlalchemy import inspect; from todo_app.db.session import engine; print(inspect(engine).get_table_names())"
# Expected: ['alembic_version', 'projects', 'tasks']
```

---

## ▶️ Run the CLI Application

Use Poetry to run the CLI app:

```bash
poetry run python main.py
```

You should see:

```text
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
```

All data is now stored in PostgreSQL via SQLAlchemy repositories.

---

## 🔁 Auto-Close Overdue Tasks

### Run as a one-off command

To immediately close all overdue tasks:

```bash
poetry run python -m todo_app.commands.autoclose_overdue
```

Output example:

```text
Auto-closed 3 overdue tasks.
```

Then you can re-run the CLI and verify that those tasks now have `status = done` and `closed_at` set.

---

## ⏱️ Run the Scheduler (Dev / Demo)

For development or during a presentation, you can run the scheduler that calls the auto-close job every **15 seconds**:

```bash
poetry run python -m todo_app.commands.scheduler
```

Expected output:

```text
[scheduler] Started. Running autoclose job every 15 seconds. Press Ctrl+C to stop.
[scheduler] Auto-closed 2 overdue tasks.
[scheduler] Auto-closed 0 overdue tasks.
...
```

* While this runs, you can keep the CLI open in another terminal and observe that overdue tasks are automatically moved to `done`.
* Press `Ctrl + C` to stop the scheduler.

---

## 🧪 Development Tips

* To reset DB completely during development:

  ```bash
  docker compose down -v
  docker compose up -d
  poetry run alembic upgrade head
  ```

* To inspect current tables or try short snippets, you can open a Python shell inside Poetry:

  ```bash
  poetry run python
  >>> from todo_app.db.session import SessionLocal
  >>> from todo_app.db.models import ProjectORM
  >>> session = SessionLocal()
  >>> session.query(ProjectORM).all()
  ```

---

## 👤 Author

**Mehdi Gholami**
📧 [m3hdigholami@aut.ac.ir](mailto:m3hdigholami@aut.ac.ir)
🔗 [GitHub Profile](https://github.com/m3hdi2gh)

---
