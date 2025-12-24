"""Project API endpoints."""

from fastapi import APIRouter, HTTPException, status

from todo_app.api.controller_schemas.project_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from todo_app.api.controller_schemas.project_response_schema import (
    ProjectListResponse,
    ProjectResponse,
)
from todo_app.api.dependencies import ProjectServiceDep

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(
    request: ProjectCreateRequest,
    service: ProjectServiceDep,
) -> ProjectResponse:
    """Create a new project with the given name and description."""
    try:
        project = service.create_project(name=request.name, description=request.description)
        return ProjectResponse.model_validate(project)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "",
    response_model=ProjectListResponse,
    summary="List all projects",
)
def list_projects(service: ProjectServiceDep) -> ProjectListResponse:
    """Retrieve all projects."""
    projects = service.list_projects()
    return ProjectListResponse(
        projects=[ProjectResponse.model_validate(p) for p in projects],
        total=len(projects),
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project by ID",
)
def get_project(project_id: str, service: ProjectServiceDep) -> ProjectResponse:
    """Retrieve a single project by its ID."""
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    return ProjectResponse.model_validate(project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
)
def update_project(
    project_id: str,
    request: ProjectUpdateRequest,
    service: ProjectServiceDep,
) -> ProjectResponse:
    """Update an existing project."""
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )

    try:
        new_name = request.name if request.name is not None else project.name
        new_desc = request.description if request.description is not None else project.description
        updated = service.edit_project(project_id, new_name=new_name, new_description=new_desc)
        return ProjectResponse.model_validate(updated)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def delete_project(project_id: str, service: ProjectServiceDep) -> None:
    """Delete a project and all its tasks."""
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    service.delete_project(project_id)