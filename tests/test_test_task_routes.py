from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api import task_routes
from app.main import app
from app.models.task import TaskCreate, TaskPriority, TaskUpdate
from app.repository.task_repository import TaskRepository
from app.services.task_service import TaskService


class FixedPriorityAdvisor:
    """Test advisor with deterministic priority."""

    def suggest(self, payload: TaskCreate | TaskUpdate) -> TaskPriority:
        return TaskPriority.high


@pytest.fixture
def client(monkeypatch) -> Generator[TestClient, None, None]:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    task_service = TaskService(
        repository=TaskRepository(),
        priority_advisor=FixedPriorityAdvisor(),
    )
    monkeypatch.setattr(task_routes, "task_service", task_service)

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def task_payload() -> dict[str, str]:
    return {
        "title": "Prepare sprint planning",
        "description": "Organize backlog items for the next sprint",
    }


def test_create_task_returns_201(
    client: TestClient,
    task_payload: dict[str, str],
) -> None:
    response = client.post("/tasks", json=task_payload)

    assert response.status_code == 201
    assert response.json()["title"] == "Prepare sprint planning"
    assert response.json()["priority"] == "high"


def test_list_tasks_returns_200(
    client: TestClient,
    task_payload: dict[str, str],
) -> None:
    created_task = client.post("/tasks", json=task_payload).json()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [created_task]


def test_get_task_by_id_returns_200(
    client: TestClient,
    task_payload: dict[str, str],
) -> None:
    created_task = client.post("/tasks", json=task_payload).json()

    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]


def test_update_task_returns_200(
    client: TestClient,
    task_payload: dict[str, str],
) -> None:
    created_task = client.post("/tasks", json=task_payload).json()

    response = client.put(
        f"/tasks/{created_task['id']}",
        json={
            "title": "Review sprint planning",
            "status": "in_progress",
            "priority": "urgent",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]
    assert response.json()["title"] == "Review sprint planning"
    assert response.json()["status"] == "in_progress"
    assert response.json()["priority"] == "urgent"


def test_delete_task_returns_204(
    client: TestClient,
    task_payload: dict[str, str],
) -> None:
    created_task = client.post("/tasks", json=task_payload).json()

    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_get_task_by_unknown_id_returns_404(client: TestClient) -> None:
    response = client.get("/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task_by_unknown_id_returns_404(client: TestClient) -> None:
    response = client.put(
        "/tasks/00000000-0000-0000-0000-000000000000",
        json={"title": "Missing task"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task_by_unknown_id_returns_404(client: TestClient) -> None:
    response = client.delete("/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
