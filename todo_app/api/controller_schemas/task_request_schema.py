"""Request schemas for Task endpoints."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


TaskStatusType = Literal["todo", "doing", "done"]


class TaskCreateRequest(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Task title (required)",
        examples=["Complete documentation"],
    )
    description: str = Field(
        default="",
        max_length=500,
        description="Task description (optional)",
    )
    deadline: date | None = Field(
        default=None,
        description="Task deadline in YYYY-MM-DD format",
        examples=["2025-12-31"],
    )
    status: TaskStatusType = Field(
        default="todo",
        description="Task status",
    )

    @field_validator("deadline")
    @classmethod
    def deadline_not_in_past(cls, v: date | None) -> date | None:
        if v is not None and v < date.today():
            raise ValueError("Deadline cannot be in the past")
        return v


class TaskUpdateRequest(BaseModel):
    """Schema for updating an existing task."""

    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    deadline: date | None = Field(default=None)
    status: TaskStatusType | None = Field(default=None)

    @field_validator("deadline")
    @classmethod
    def deadline_not_in_past(cls, v: date | None) -> date | None:
        if v is not None and v < date.today():
            raise ValueError("Deadline cannot be in the past")
        return v


class TaskStatusUpdateRequest(BaseModel):
    """Schema for updating only task status."""

    status: TaskStatusType = Field(..., description="New task status")