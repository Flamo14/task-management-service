import uuid
from typing import List, Optional

from src.domain.task import Task
from src.domain.task_status import TaskStatus
from src.repositories.task_repository import TaskRepository


class TaskValidationError(Exception):
    """Raised when task validation fails."""
    pass


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create(self, task: Task) -> Task:
        """
        Create a new task with validation and defaults.
        
        Args:
            task: Task object to create
            
        Returns:
            Created task with assigned id and defaults applied
            
        Raises:
            TaskValidationError: If task.title is empty
        """
        # Validate title is not empty
        if not task.title or not task.title.strip():
            raise TaskValidationError("Task title cannot be empty")
        
        # Assign unique id if not provided
        task_id = task.id if task.id else str(uuid.uuid4())
        
        # Set status to "pending" if not set
        status = task.status if task.status else TaskStatus.PENDING
        
        # Create processed task with validated/default values
        processed_task = Task(
            id=task_id,
            title=task.title.strip(),
            description=task.description,
            status=status,
            priority=task.priority,
            start_date=task.start_date,
            end_date=task.end_date
        )
        
        # Persist and return
        return self._repository.create(processed_task)

    def get_all(self) -> List[Task]:
        """Retrieve all tasks from the repository."""
        return self._repository.get_all()

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID from the repository."""
        return self._repository.get_by_id(task_id)

    def update(self, task: Task) -> Optional[Task]:
        """Update an existing task with provided values."""
        if not task.id or not task.id.strip():
            raise TaskValidationError("Task id is required")

        existing_task = self._repository.get_by_id(task.id)
        if existing_task is None:
            return None

        updated_task = Task(
            id=existing_task.id,
            title=task.title if task.title is not None else existing_task.title,
            description=task.description if task.description is not None else existing_task.description,
            status=task.status if task.status is not None else existing_task.status,
            priority=task.priority if task.priority is not None else existing_task.priority,
            start_date=task.start_date if task.start_date is not None else existing_task.start_date,
            end_date=task.end_date if task.end_date is not None else existing_task.end_date,
        )

        return self._repository.update(updated_task)

    def delete(self, task_id: str) -> bool:
        if not task_id or not task_id.strip():
            raise TaskValidationError("Task id is required")

        existing_task = self._repository.get_by_id(task_id)
        if existing_task is None:
            return False

        self._repository.delete(task_id)
        return True
