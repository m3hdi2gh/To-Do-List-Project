"""Request schemas for Project endpoints."""

from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Project name (required)",
        examples=["My Project"],
    )
    description: str = Field(
        default="",
        max_length=500,
        description="Project description (optional)",
        examples=["A sample project description"],
    )


class ProjectUpdateRequest(BaseModel):
    """Schema for updating an existing project."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="New project name",
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="New project description",
    )