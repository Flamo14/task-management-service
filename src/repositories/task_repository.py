from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task: Task) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        raise NotImplementedError
