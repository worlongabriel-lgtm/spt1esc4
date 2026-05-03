from uuid import uuid4

import pytest

from app.models.task import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.repository.task_repository import TaskRepository
from app.services.task_service import TaskService


class FixedPriorityAdvisor:
    """Test advisor with deterministic priority."""

    def suggest(self, payload: TaskCreate | TaskUpdate) -> TaskPriority:
        return TaskPriority.high


@pytest.fixture
def task_service() -> TaskService:
    return TaskService(
        repository=TaskRepository(),
        priority_advisor=FixedPriorityAdvisor(),
    )


@pytest.fixture
def task_payload() -> TaskCreate:
    return TaskCreate(
        title="Prepare sprint planning",
        description="Organize backlog items for the next sprint",
    )


def test_create_task_returns_task_with_generated_fields(
    task_service: TaskService,
    task_payload: TaskCreate,
) -> None:
    task = task_service.create(task_payload)

    assert task.id is not None
    assert task.title == "Prepare sprint planning"
    assert task.description == "Organize backlog items for the next sprint"
    assert task.status == TaskStatus.pending
    assert task.priority == TaskPriority.high
    assert task.created_at == task.updated_at


def test_list_tasks_returns_created_tasks(
    task_service: TaskService,
    task_payload: TaskCreate,
) -> None:
    task = task_service.create(task_payload)

    tasks = task_service.list()

    assert tasks == [task]


def test_get_by_id_returns_existing_task(
    task_service: TaskService,
    task_payload: TaskCreate,
) -> None:
    created_task = task_service.create(task_payload)

    task = task_service.get_by_id(created_task.id)

    assert task == created_task


def test_get_by_id_returns_none_when_task_does_not_exist(
    task_service: TaskService,
) -> None:
    task = task_service.get_by_id(uuid4())

    assert task is None


def test_update_task_changes_existing_task(
    task_service: TaskService,
    task_payload: TaskCreate,
) -> None:
    created_task = task_service.create(task_payload)
    payload = TaskUpdate(
        title="Review sprint planning",
        status=TaskStatus.in_progress,
        priority=TaskPriority.urgent,
    )

    updated_task = task_service.update(created_task.id, payload)

    assert updated_task is not None
    assert updated_task.id == created_task.id
    assert updated_task.title == "Review sprint planning"
    assert updated_task.description == created_task.description
    assert updated_task.status == TaskStatus.in_progress
    assert updated_task.priority == TaskPriority.urgent
    assert updated_task.created_at == created_task.created_at
    assert updated_task.updated_at >= created_task.updated_at


def test_update_task_returns_none_when_task_does_not_exist(
    task_service: TaskService,
) -> None:
    payload = TaskUpdate(title="Missing task")

    updated_task = task_service.update(uuid4(), payload)

    assert updated_task is None


def test_delete_task_removes_existing_task(
    task_service: TaskService,
    task_payload: TaskCreate,
) -> None:
    created_task = task_service.create(task_payload)

    deleted = task_service.delete(created_task.id)

    assert deleted is True
    assert task_service.get_by_id(created_task.id) is None
    assert task_service.list() == []


def test_delete_task_returns_false_when_task_does_not_exist(
    task_service: TaskService,
) -> None:
    deleted = task_service.delete(uuid4())

    assert deleted is False
