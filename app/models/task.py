from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(StrEnum):
    """Allowed task statuses."""

    pending = "pending"
    in_progress = "in_progress"
    done = "done"
    canceled = "canceled"


class TaskPriority(StrEnum):
    """Allowed task priorities."""

    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TaskBase(BaseModel):
    """Shared task fields."""

    title: str = Field(min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("title must not be empty")
        return title

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is None:
            return value

        description = value.strip()
        return description or None

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: datetime | None) -> datetime | None:
        if value is not None and value < datetime.now(UTC):
            raise ValueError("due_date must be in the future")
        return value


class TaskCreate(TaskBase):
    """Payload for creating a task."""


class TaskUpdate(BaseModel):
    """Payload for updating a task."""

    title: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        title = value.strip()
        if not title:
            raise ValueError("title must not be empty")
        return title

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is None:
            return value

        description = value.strip()
        return description or None

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: datetime | None) -> datetime | None:
        if value is not None and value < datetime.now(UTC):
            raise ValueError("due_date must be in the future")
        return value


class TaskOut(TaskBase):
    """Task response model."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
