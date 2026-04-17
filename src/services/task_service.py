from typing import List, Optional

from src.domain.task import Task
from src.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create(self, task: Task) -> Task:
        pass

    def get_all(self) -> List[Task]:
        pass

    def get_by_id(self, task_id: str) -> Optional[Task]:
        pass

    def update(self, task: Task) -> Optional[Task]:
        pass

    def delete(self, task_id: str) -> bool:
        pass
