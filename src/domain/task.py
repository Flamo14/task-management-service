from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Task:
    id: str
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "normal"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
