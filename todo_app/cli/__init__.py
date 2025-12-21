"""
CLI module for ToDoList application.

.. deprecated::
    The CLI interface is deprecated and will be removed in a future release.
    Please use the FastAPI-based Web API instead.

    To run the API:
        uvicorn todo_app.api.main:app --reload

    API documentation available at:
        http://localhost:8000/docs
"""

from .console import run_cli