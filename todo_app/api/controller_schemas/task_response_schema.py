"""Response schemas for Task endpoints."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TaskStatusType = Literal["todo", "doing", "done"]


class TaskResponse(BaseModel):
    """Schema for a single task response."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., examples=["550e8400-e29b-41d4-a716-446655440000"])
    title: str = Field(..., examples=["Complete documentation"])
    description: str = Field(..., examples=["Write API docs"])
    deadline: date | None = Field(default=None, examples=["2025-12-31"])
    status: TaskStatusType = Field(..., examples=["todo"])


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""

    tasks: list[TaskResponse]
    total: int = Field(..., description="Total number of tasks")