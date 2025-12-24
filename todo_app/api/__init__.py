"""
FastAPI Web API for ToDo List application.

This module provides RESTful endpoints for managing projects and tasks,
replacing the deprecated CLI interface.
"""

from todo_app.api.main import app, create_app

__all__ = ["app", "create_app"]