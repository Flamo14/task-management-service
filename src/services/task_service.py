from datetime import date
from typing import List, Optional

from src.domain.task import Task
from src.domain.task_status import TaskStatus
from src.repositories.task_repository import TaskRepository
from src.services.create_task.task_factory import TaskFactory


class TaskValidationError(Exception):
    """Raised when task validation fails."""
    pass


def create_task(
    title: str,
    user_id: str,
    description: Optional[str] = None,
    priority: str = "normal",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Task:
    """
    Pure function to create a validated task.
    
    Characteristics:
    - No side effects (doesn't modify external state or perform I/O)
    - Deterministic: same input always produces same output
    - No external dependencies on state
    
    Responsibilities:
    - Validate business rules (title and user_id must not be empty)
    - Delegate object creation to TaskFactory
    
    Args:
        title: Task title (must not be empty/whitespace)
        user_id: User ID (must not be empty/whitespace)
        description: Optional task description
        priority: Task priority (default: "normal")
        start_date: Optional start date
        end_date: Optional end date
    
    Returns:
        Task: A validated Task instance with generated ID and defaults
    
    Raises:
        TaskValidationError: If title or user_id is empty/invalid
    """
    # Validate title
    if not title or not title.strip():
        raise TaskValidationError("Task title cannot be empty")
    
    # Validate user_id
    if not user_id or not user_id.strip():
        raise TaskValidationError("Task user_id cannot be empty")
    
    # Delegate to factory for object creation
    return TaskFactory.create(
        title=title.strip(),
        user_id=user_id.strip(),
        description=description,
        priority=priority,
        start_date=start_date,
        end_date=end_date,
    )


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create(
        self,
        title: str,
        user_id: str,
        description: Optional[str] = None,
        priority: str = "normal",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Task:
        """
        Create a new task with validation and persistence.
        
        Uses the pure create_task function for business logic,
        then persists the result to the repository.
        
        Args:
            title: Task title (must not be empty/whitespace)
            user_id: User ID (must not be empty/whitespace)
            description: Optional task description
            priority: Task priority (default: "normal")
            start_date: Optional start date
            end_date: Optional end date
        
        Returns:
            Created task persisted to repository
        
        Raises:
            TaskValidationError: If title or user_id is empty
        """
        # Use pure function for business logic
        task = create_task(
            title=title,
            user_id=user_id,
            description=description,
            priority=priority,
            start_date=start_date,
            end_date=end_date,
        )
        
        # Persist and return
        return self._repository.create(task)

    def get_all(self, user_id: str) -> List[Task]:
        """Retrieve all tasks for a specific user from the repository."""
        return self._repository.get_by_user_id(user_id)

    def get_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """Retrieve a task by its ID only if it belongs to the specified user."""
        task = self._repository.get_by_id(task_id)
        if task is None or task.user_id != user_id:
            return None
        return task

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
