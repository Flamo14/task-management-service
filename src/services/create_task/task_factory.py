from uuid import uuid4
from typing import Optional
from datetime import date

from src.domain.task import Task
from src.domain.task_status import TaskStatus


class TaskFactory:
    """
    Factory responsible for creating Task objects.
    
    Responsibilities:
    - Generate unique task IDs
    - Assign default status to tasks
    - Create Task instances with consistent defaults
    
    This factory encapsulates task object creation logic, keeping it separate
    from business validation (which resides in TaskService).
    """

    @staticmethod
    def create(
        title: str,
        user_id: str,
        description: Optional[str] = None,
        priority: str = "normal",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: Optional[TaskStatus] = None,
    ) -> Task:
        """
        Create a new Task instance with a generated unique ID and defaults.
        
        Does NOT perform business validation - that is delegated to TaskService.
        Focus is purely on object creation and assigning defaults.
        
        Args:
            title: Task title
            user_id: Task owner's user ID
            description: Optional task description
            priority: Task priority (default: "normal")
            start_date: Optional start date
            end_date: Optional end date
            status: Optional task status (default: TaskStatus.PENDING)
        
        Returns:
            Task: A new Task instance with generated ID and defaults applied
        """
        task_id = str(uuid4())
        final_status = status if status else TaskStatus.PENDING

        return Task(
            id=task_id,
            title=title,
            user_id=user_id,
            description=description,
            status=final_status,
            priority=priority,
            start_date=start_date,
            end_date=end_date,
        )
