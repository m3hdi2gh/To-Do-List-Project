"""Task API endpoints."""

from fastapi import APIRouter, HTTPException, status

from todo_app.api.controller_schemas.task_request_schema import (
    TaskCreateRequest,
    TaskStatusUpdateRequest,
    TaskUpdateRequest,
)
from todo_app.api.controller_schemas.task_response_schema import (
    TaskListResponse,
    TaskResponse,
)
from todo_app.api.dependencies import TaskServiceDep

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(
    project_id: str,
    request: TaskCreateRequest,
    service: TaskServiceDep,
) -> TaskResponse:
    """Create a new task within a project."""
    try:
        # Convert date to string for service
        deadline_str = request.deadline.isoformat() if request.deadline else None
        task = service.add_task(
            project_id=project_id,
            title=request.title,
            description=request.description,
            deadline_str=deadline_str,
            status=request.status,
        )
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "",
    response_model=TaskListResponse,
    summary="List all tasks in a project",
)
def list_tasks(project_id: str, service: TaskServiceDep) -> TaskListResponse:
    """Retrieve all tasks for a specific project."""
    try:
        tasks = service.list_tasks_of_project(project_id)
        return TaskListResponse(
            tasks=[TaskResponse.model_validate(t) for t in tasks],
            total=len(tasks),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
)
def get_task(project_id: str, task_id: str, service: TaskServiceDep) -> TaskResponse:
    """Retrieve a single task by its ID."""
    # Find task in the project's tasks
    tasks = service.list_tasks_of_project(project_id)
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found in project {project_id}",
        )
    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update_task(
    project_id: str,
    task_id: str,
    request: TaskUpdateRequest,
    service: TaskServiceDep,
) -> TaskResponse:
    """Update an existing task."""
    # First check if task exists
    tasks = service.list_tasks_of_project(project_id)
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found in project {project_id}",
        )

    try:
        deadline_str = request.deadline.isoformat() if request.deadline else None
        updated = service.edit_task(
            task_id,
            title=request.title if request.title is not None else None,
            description=request.description if request.description is not None else None,
            deadline_str=deadline_str,
            status=request.status if request.status is not None else None,
        )
        return TaskResponse.model_validate(updated)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="Update task status",
)
def update_task_status(
    project_id: str,
    task_id: str,
    request: TaskStatusUpdateRequest,
    service: TaskServiceDep,
) -> TaskResponse:
    """Update only the status of a task."""
    # First check if task exists
    tasks = service.list_tasks_of_project(project_id)
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found in project {project_id}",
        )

    try:
        updated = service.change_status(task_id, request.status)
        return TaskResponse.model_validate(updated)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(project_id: str, task_id: str, service: TaskServiceDep) -> None:
    """Delete a task from a project."""
    # First check if task exists
    tasks = service.list_tasks_of_project(project_id)
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found in project {project_id}",
        )
    service.delete_task(task_id)