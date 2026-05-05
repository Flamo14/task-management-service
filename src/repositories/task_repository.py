from abc import ABC, abstractmethod
from typing import Dict, List, Optional

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
    def get_by_user_id(self, user_id: str) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task: Task) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        raise NotImplementedError


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}

    def create(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def get_all(self) -> List[Task]:
        return list(self._tasks.values())

    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def get_by_user_id(self, user_id: str) -> List[Task]:
        return [task for task in self._tasks.values() if task.user_id == user_id]

    def update(self, task: Task) -> Optional[Task]:
        if task.id not in self._tasks:
            return None
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> bool:
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True
