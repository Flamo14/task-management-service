from abc import ABC, abstractmethod
from typing import Dict, Optional

from src.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}

    def create(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
