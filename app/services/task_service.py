from uuid import UUID

from app.models.task import TaskCreate, TaskOut, TaskUpdate
from app.repository.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor


class TaskService:
    """Coordinates task business rules."""

    def __init__(
        self,
        repository: TaskRepository,
        priority_advisor: PriorityAdvisor,
    ) -> None:
        self._repository = repository
        self._priority_advisor = priority_advisor

    def create(self, payload: TaskCreate) -> TaskOut:
        priority = self._priority_advisor.suggest(payload)
        task_data = payload.model_copy(update={"priority": priority})
        return self._repository.create(task_data)

    def list(self) -> list[TaskOut]:
        return self._repository.list()

    def get_by_id(self, task_id: UUID) -> TaskOut | None:
        return self._repository.get_by_id(task_id)

    def update(self, task_id: UUID, payload: TaskUpdate) -> TaskOut | None:
        update_data = payload

        if payload.priority is None:
            suggested_priority = self._priority_advisor.suggest(payload)
            update_data = payload.model_copy(update={"priority": suggested_priority})

        return self._repository.update(task_id, update_data)

    def delete(self, task_id: UUID) -> bool:
        return self._repository.delete(task_id)
