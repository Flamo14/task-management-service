import pytest

from src.domain.user import User
from src.repositories.user_repository import InMemoryUserRepository
from src.services.user_service import UserService


def test_authenticate_success():
    repo = InMemoryUserRepository()
    service = UserService(repo)

    email = "alice@example.com"
    password = "s3cret"

    registered = service.register(email, password)

    authenticated = service.authenticate(email, password)

    assert authenticated is not None
    assert authenticated == registered


def test_authenticate_wrong_password():
    repo = InMemoryUserRepository()
    service = UserService(repo)

    email = "bob@example.com"
    password = "password123"

    service.register(email, password)

    assert service.authenticate(email, "wrongpass") is None


def test_authenticate_unknown_email():
    repo = InMemoryUserRepository()
    service = UserService(repo)

    assert service.authenticate("noone@example.com", "doesntmatter") is None
