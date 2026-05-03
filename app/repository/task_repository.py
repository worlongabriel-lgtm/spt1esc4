from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.models.task import TaskCreate, TaskOut, TaskUpdate


class TaskRepository:
    """In-memory task repository."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, TaskOut] = {}

    def create(self, payload: TaskCreate) -> TaskOut:
        now = datetime.now(UTC)
        task = TaskOut(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )

        self._tasks[task.id] = task
        return task

    def list(self) -> list[TaskOut]:
        return list(self._tasks.values())

    def get_by_id(self, task_id: UUID) -> TaskOut | None:
        return self._tasks.get(task_id)

    def update(self, task_id: UUID, payload: TaskUpdate) -> TaskOut | None:
        task = self.get_by_id(task_id)
        if task is None:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        updated_task = task.model_copy(
            update={
                **update_data,
                "updated_at": datetime.now(UTC),
            },
        )

        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: UUID) -> bool:
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True
