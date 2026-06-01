import pytest

from src.domain.task import Task
from src.domain.task_status import TaskStatus
from src.repositories.task_repository import InMemoryTaskRepository
from src.services.task_service import TaskService


def test_update_task_preserves_user_id_and_updates_fields():
    repository = InMemoryTaskRepository()
    service = TaskService(repository)

    original = service.create(
        title="Initial task",
        user_id="user-123",
        description="Original description",
        priority="normal",
    )

    updated = service.update(
        Task(
            id=original.id,
            title="Updated task",
            user_id=original.user_id,
            description="Updated description",
            status=TaskStatus.DONE,
            priority="high",
        )
    )

    assert updated is not None
    assert updated.id == original.id
    assert updated.user_id == original.user_id
    assert updated.title == "Updated task"
    assert updated.description == "Updated description"
    assert updated.status == TaskStatus.DONE
    assert updated.priority == "high"


def test_update_task_preserves_existing_fields_when_none_passed():
    repository = InMemoryTaskRepository()
    service = TaskService(repository)

    original = service.create(
        title="Keep fields",
        user_id="user-456",
        description="Keep this",
        priority="low",
    )

    updated = service.update(
        Task(
            id=original.id,
            title=None,
            user_id=original.user_id,
            description=None,
            status=None,
            priority=None,
        )
    )

    assert updated is not None
    assert updated.title == original.title
    assert updated.description == original.description
    assert updated.status == original.status
    assert updated.priority == original.priority
