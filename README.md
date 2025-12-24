# 📝 To-Do List App (Python OOP — FastAPI & PostgreSQL)

A **To-Do List application** built with:

- **Clean Python OOP domain models** (`Project`, `Task`)
- **Repository pattern** (in-memory + SQLAlchemy)
- **PostgreSQL** for persistence
- **Alembic** for database migrations
- **FastAPI** RESTful Web API
- A simple **scheduler** to auto-close overdue tasks
- **Postman collection & environment** for API testing (Phase 4)

This project is developed incrementally in four phases:

- **Phase 1** → Pure CLI + in-memory storage  
- **Phase 2** → Persistence layer with PostgreSQL, SQLAlchemy ORM, Alembic, and background scheduling
- **Phase 3** → RESTful Web API with FastAPI
- **Phase 4 (current)** → Postman workspace/collection for testing and demo

---

## 🚀 Main Features

### 🌐 RESTful Web API (Phase 3)
- Full CRUD operations for Projects and Tasks via HTTP endpoints
- Interactive API documentation (Swagger UI & ReDoc)
- Pydantic request/response validation
- Dependency injection for services and database sessions
- Proper HTTP status codes and error handling

### 🧪 Postman Testing (Phase 4)
- A complete **Postman Collection** and **Environment** are provided under `postman/`
- Collection contains requests for:
  - Health check
  - Project CRUD
  - Task CRUD (under a project)
  - Patch task status
- Uses environment variables:
  - `{{base_url}}`, `{{project_id}}`, `{{task_id}}`
- Designed for a clean demo scenario:
  1) Create Project → saves `project_id`
  2) Create Task → saves `task_id`
  3) List/Get/Update/Patch/Delete Task
  4) Delete Project

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
- Clear error messages

### 🗄️ Persistence & Migrations
- **PostgreSQL** as the main data store (via `docker-compose`)
- **SQLAlchemy ORM** models
- **Alembic** for schema migrations
- IDs are stored as `UUID` strings (length 36)

### ⏱️ Auto-Close Overdue Tasks
- Management command: `poetry run python -m todo_app.commands.autoclose_overdue`
- Finds tasks with `deadline < today` and `status != "done"`
- Sets `status = "done"` and updates `closed_at`

### 🕒 Simple Scheduler
- Command: `poetry run python -m todo_app.commands.scheduler`
- Runs auto-close job every 15 seconds (configurable)

---

## 🌐 API Documentation

### Running the API Server
```bash
poetry run uvicorn todo_app.api.main:app --reload
````

The API will be available at: `http://127.0.0.1:8000`

### Interactive Documentation

* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### API Endpoints

#### Health Check

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| GET    | `/`      | API health status |

#### Projects

| Method | Endpoint                 | Description          |
| ------ | ------------------------ | -------------------- |
| GET    | `/projects`              | List all projects    |
| POST   | `/projects`              | Create a new project |
| GET    | `/projects/{project_id}` | Get a project by ID  |
| PUT    | `/projects/{project_id}` | Update a project     |
| DELETE | `/projects/{project_id}` | Delete a project     |

#### Tasks

| Method | Endpoint                                        | Description                 |
| ------ | ----------------------------------------------- | --------------------------- |
| GET    | `/projects/{project_id}/tasks`                  | List all tasks in a project |
| POST   | `/projects/{project_id}/tasks`                  | Create a new task           |
| GET    | `/projects/{project_id}/tasks/{task_id}`        | Get a task by ID            |
| PUT    | `/projects/{project_id}/tasks/{task_id}`        | Update a task               |
| PATCH  | `/projects/{project_id}/tasks/{task_id}/status` | Update task status only     |
| DELETE | `/projects/{project_id}/tasks/{task_id}`        | Delete a task               |

---

## 📬 Postman (Phase 4)

### Files

Postman artifacts are located in:

```text
postman/
  ├── postman_collection.json
  └── postman_environment.json
```

### Import in Postman

1. Open Postman → **Import**
2. Import `postman/postman_collection.json`
3. Import `postman/postman_environment.json`
4. Select the environment (top-right) and set:

   * `base_url = http://127.0.0.1:8000`

### Recommended Run Order (Demo)

Run requests in this order:

1. `GET /` (Health)
2. `POST /projects` (stores `project_id`)
3. `POST /projects/{{project_id}}/tasks` (stores `task_id`)
4. Task operations (List/Get/Update/Patch/Delete)
5. `DELETE /projects/{{project_id}}`

> Note: Create-requests use Postman scripts to automatically store IDs into the environment variables.

---

## 🧠 Architecture Overview

### API Layer (`todo_app/api`) - Phase 3

* **`main.py`** - FastAPI application factory with health check endpoint
* **`router.py`** - Central router combining all controllers
* **`dependencies.py`** - Dependency injection for DB sessions and services
* **`controllers/`** - HTTP endpoint handlers

  * `projects_controller.py` - Project CRUD endpoints
  * `tasks_controller.py` - Task CRUD endpoints
* **`controller_schemas/`** - Pydantic models for request/response validation

  * `project_request_schema.py` / `project_response_schema.py`
  * `task_request_schema.py` / `task_response_schema.py`

### Domain Layer (`todo_app/models`)

* **`Project`** - Fields: `id`, `name`, `description`, `created_at`, `tasks`
* **`Task`** - Fields: `id`, `title`, `description`, `status`, `deadline`, `created_at`

### Persistence Layer (`todo_app/db`, `todo_app/repositories`)

* **ORM Models**: `ProjectORM`, `TaskORM`
* **Repositories**: `SqlAlchemyProjectRepository`, `SqlAlchemyTaskRepository`

### Services (`todo_app/services`)

* **ProjectService** - Project business logic
* **TaskService** - Task business logic

### CLI Layer (`todo_app/cli`) - Deprecated

> ⚠️ The CLI interface is deprecated. Please use the Web API instead.

---

## 🏗️ Project Structure

```text
├── todo_app/
│   ├── api/                   # FastAPI Web API (Phase 3)
│   ├── cli/                   # CLI interface (deprecated)
│   ├── commands/              # Management commands
│   ├── config/                # Settings
│   ├── db/                    # SQLAlchemy + Session
│   ├── models/                # Domain models
│   ├── repositories/          # Repository implementations
│   ├── services/              # Business logic
│   └── exceptions/
│
├── postman/                   # Postman artifacts (Phase 4)
│   ├── postman_collection.json
│   └── postman_environment.json
│
├── alembic/
├── docker-compose.yml
├── alembic.ini
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── main.py
```

---

## ⚙️ Environment & Configuration

### Create `.env` file

```bash
cp .env.example .env
```

Default values:

```env
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=100

DB_HOST=localhost
DB_PORT=5432
DB_NAME=todolist
DB_USER=todolist_user
DB_PASSWORD=todolist_password
```

---

## 📦 Installation

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

```bash
docker compose up -d
```

To stop and clean:

```bash
docker compose down -v
```

---

## 🔁 Apply Database Migrations

```bash
poetry run alembic upgrade head
```

---

## ▶️ Run the Application

### Web API (Recommended)

```bash
poetry run uvicorn todo_app.api.main:app --reload
```

Then open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### CLI (Deprecated)

```bash
poetry run python main.py
```

> ⚠️ The CLI is deprecated. Please use the Web API.

---

## 🔁 Auto-Close Overdue Tasks

```bash
poetry run python -m todo_app.commands.autoclose_overdue
```

---

## ⏱️ Run the Scheduler

```bash
poetry run python -m todo_app.commands.scheduler
```

---

## 🧪 Development Tips

Reset DB:

```bash
docker compose down -v
docker compose up -d
poetry run alembic upgrade head
```

---

## 👤 Author

**Mehdi Gholami**
📧 [m3hdigholami@aut.ac.ir](mailto:m3hdigholami@aut.ac.ir)
🔗 [GitHub Profile](https://github.com/m3hdi2gh)
