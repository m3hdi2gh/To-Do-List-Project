"""Response schemas for Project endpoints."""

from pydantic import BaseModel, ConfigDict, Field


class ProjectResponse(BaseModel):
    """Schema for a single project response."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., examples=["550e8400-e29b-41d4-a716-446655440000"])
    name: str = Field(..., examples=["My Project"])
    description: str = Field(..., examples=["Project description"])


class ProjectListResponse(BaseModel):
    """Schema for list of projects response."""

    projects: list[ProjectResponse]
    total: int = Field(..., description="Total number of projects")