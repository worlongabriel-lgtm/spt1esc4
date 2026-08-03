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


def test_health_check_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "timestamp" in response.json()


def test_list_tasks_supports_filters(
    client: TestClient,
    task_payload: dict[str, str],
) -> None:
    first_task = client.post("/tasks", json=task_payload).json()
    second_task = client.post(
        "/tasks",
        json={
            "title": "Revisar documento",
            "description": "Analisar as notas da reunião",
            "due_date": "2099-12-31T00:00:00Z",
        },
    ).json()

    client.put(
        f"/tasks/{second_task['id']}",
        json={"status": "in_progress", "priority": "urgent"},
    )

    response_by_status = client.get("/tasks", params={"status": "in_progress"})
    assert response_by_status.status_code == 200
    assert len(response_by_status.json()) == 1
    assert response_by_status.json()[0]["id"] == second_task["id"]

    response_by_priority = client.get("/tasks", params={"priority": "urgent"})
    assert response_by_priority.status_code == 200
    assert len(response_by_priority.json()) == 1
    assert response_by_priority.json()[0]["id"] == second_task["id"]

    response_by_due_date = client.get(
        "/tasks",
        params={"due_date": "2099-12-31T00:00:00Z"},
    )
    assert response_by_due_date.status_code == 200
    assert len(response_by_due_date.json()) == 1
    assert response_by_due_date.json()[0]["id"] == second_task["id"]


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
