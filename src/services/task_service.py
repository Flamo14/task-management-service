from typing import List, Optional

from src.domain.task import Task
from src.domain.task_status import TaskStatus
from src.repositories.task_repository import TaskRepository


class TaskValidationError(Exception):
    """Raised when task validation fails."""
    pass


# Pure Function: Deterministic, no side effects, no UUID generation
def build_created_task(
    title: str,
    user_id: str,
    task_id: str,
    description: Optional[str] = None,
    priority: str = "normal",
    start_date: Optional[object] = None,
    end_date: Optional[object] = None,
    status: Optional[TaskStatus] = None,
) -> Optional[Task]:
    """
    Pure function to build a validated task with defaults applied.
    
    Deterministic:
    - No UUID generation (task_id must be provided)
    - No datetime/random values
    - Always produces the same output for the same input
    - No external service calls or side effects
    
    Args:
        title: Task title (must not be empty/whitespace)
        user_id: User ID (must not be empty/whitespace)
        task_id: Task ID (must not be empty/whitespace, or returns None)
        description: Optional task description
        priority: Task priority (default: "normal")
        start_date: Optional start date
        end_date: Optional end date
        status: Optional task status (default: TaskStatus.PENDING)
    
    Returns:
        Task: A validated Task object with defaults applied, or None if task_id is missing
    
    Raises:
        TaskValidationError: If title or user_id is empty/invalid
    """
    # Validate title
    if not title or not title.strip():
        raise TaskValidationError("Task title cannot be empty")
    
    # Validate user_id
    if not user_id or not user_id.strip():
        raise TaskValidationError("Task user_id cannot be empty")
    
    # Return None if task_id is missing (do NOT generate it)
    if not task_id or not task_id.strip():
        return None
    
    # Set default status if not provided
    final_status = status if status else TaskStatus.PENDING
    
    # Create and return task with normalized values
    return Task(
        id=task_id,
        title=title.strip(),
        user_id=user_id,
        description=description,
        status=final_status,
        priority=priority,
        start_date=start_date,
        end_date=end_date,
    )


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create(self, task: Task) -> Task:
        """
        Create a new task with validation and defaults.
        
        Uses the pure function build_created_task for business logic,
        then persists the result.
        
        Args:
            task: Task object to create
            
        Returns:
            Created task with assigned id and defaults applied
            
        Raises:
            TaskValidationError: If task.title, user_id, or id is empty
        """
        # Use pure function for task creation logic
        created_task = build_created_task(
            title=task.title,
            user_id=task.user_id,
            task_id=task.id,
            description=task.description,
            priority=task.priority,
            start_date=task.start_date,
            end_date=task.end_date,
            status=task.status,
        )
        
        # If pure function returned None (task_id was missing), raise error
        if created_task is None:
            raise TaskValidationError("Task id cannot be empty")
        
        # Persist and return
        return self._repository.create(created_task)

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
