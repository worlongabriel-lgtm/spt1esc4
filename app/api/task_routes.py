from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from app.models.task import (
    TaskCreate,
    TaskOut,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)
from app.repository.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])

task_service = TaskService(
    repository=TaskRepository(),
    priority_advisor=PriorityAdvisor(),
)


@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate) -> TaskOut:
    """Create a task."""
    return task_service.create(payload)


@router.get(
    "",
    response_model=list[TaskOut],
    status_code=status.HTTP_200_OK,
)
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    due_date: datetime | None = None,
) -> list[TaskOut]:
    """List tasks with optional filters."""
    return task_service.list(
        status=status,
        priority=priority,
        due_date=due_date,
    )


@router.get(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
def get_task(task_id: UUID) -> TaskOut:
    """Get a task by ID."""
    task = task_service.get_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
def update_task(task_id: UUID, payload: TaskUpdate) -> TaskOut:
    """Update a task."""
    task = task_service.update(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: UUID) -> Response:
    """Delete a task."""
    deleted = task_service.delete(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
