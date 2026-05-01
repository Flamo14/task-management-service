import uuid
from typing import List, Optional

from src.domain.task import Task
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
        status = task.status if task.status else "pending"
        
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
        pass

    def update(self, task: Task) -> Optional[Task]:
        pass

    def delete(self, task_id: str) -> bool:
        pass
