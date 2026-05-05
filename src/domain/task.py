from dataclasses import dataclass
from datetime import date
from typing import Optional

from .task_status import TaskStatus

@dataclass
class Task:
    id: str
    title: str
    user_id: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: str = "normal"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
