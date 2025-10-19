# 📝 To-Do List App (Python OOP — In-Memory)

A command-line **To-Do List application** built with **Python OOP principles** and **In-Memory storage**.  
This project is part of an incremental and agile development process — starting simple with a CLI and evolving later toward persistence (database) and a web API (FastAPI).

---

## 🚀 Features

### 🧩 Project Management
- Create new projects with name and description  
- Edit project details  
- Delete projects (with cascade deletion of tasks)  
- List all existing projects  

### ✅ Task Management
- Add tasks to projects  
- Edit or delete tasks  
- Change task status (`todo`, `doing`, `done`)  
- View all tasks within a selected project  

### ⚙️ Configuration
- Dynamic environment variables managed via `.env` file  
  (e.g., `MAX_NUMBER_OF_PROJECT`, `MAX_NUMBER_OF_TASK`)  
- Clear error messages and user-friendly CLI interactions  

---

## 🧠 Tech Stack

| Layer | Description |
|-------|--------------|
| **Core** | Domain models (`Project`, `Task`) and business logic |
| **Services** | Handles operations, validation, and limits |
| **Storage** | In-memory repository layer for temporary data |
| **CLI** | Interactive command-line interface for user interaction |
| **Config** | Loads and manages environment variables (`python-dotenv`) |

---

## 🏗️ Project Structure

```

├── todo_app/
│   ├── core/                  # Core business logic
│   │   ├── project.py         # Project model
│   │   └── task.py            # Task model
│   ├── services/              # Business service layer
│   │   ├── project_service.py # Project management logic
│   │   └── task_service.py    # Task management logic
│   ├── storage/               # In-memory repository
│   │   └── in_memory_repo.py
│   ├── cli/                   # CLI entry point
│   │   └── main_cli.py
│   └── config/                # Environment configuration
│       └── settings.py
│
├── .env                       # Environment variables (not committed)
├── .env.example               # Example environment config
├── pyproject.toml             # Poetry dependency configuration
├── README.md                  # Documentation (this file)
└── main.py                    # Entry point for running the app

````

---

## ⚡ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/m3hdi2gh/To-Do-List-Project.git
cd To-Do-List-Project
````

### 2️⃣ Install dependencies using Poetry

```bash
poetry install
```

### 3️⃣ Activate the virtual environment

```bash
poetry env info --path
```

Copy the path and activate it (on PowerShell):

```bash
& "<venv_path>\Scripts\Activate.ps1"
```

### 4️⃣ Create `.env` file

Copy `.env.example` to `.env` and set your values:

```bash
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=20
```

---

## ▶️ Run the Application

Use Poetry to run the CLI app:

```bash
poetry run python main.py
```

Example run:

```
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

---

## 👤 Author

**Mehdi Gholami**
📧 [m3hdigholami@aut.ac.ir](mailto:m3hdigholami@aut.ac.ir)
🔗 [GitHub Profile](https://github.com/m3hdi2gh)

---
