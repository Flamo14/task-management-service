import uuid
from typing import Optional

import bcrypt

from src.domain.user import User
from src.repositories.user_repository import UserRepository


class UserRegistrationError(Exception):
    """Raised when user registration fails."""
    pass


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def register(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Created User object
            
        Raises:
            UserRegistrationError: If email is invalid or already exists
        """
        # Validate email
        if not self._is_valid_email(email):
            raise UserRegistrationError("Invalid email address")

        # Check if email already exists
        existing_user = self._repository.get_by_email(email)
        if existing_user is not None:
            raise UserRegistrationError("Email already registered")

        # Create new user with hashed password
        user_id = str(uuid.uuid4())
        # bcrypt expects bytes
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # store hashed password as utf-8 string
        user = User(id=user_id, email=email, password=hashed.decode("utf-8"))

        return self._repository.create(user)

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self._repository.get_by_id(user_id)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            email: User's email address
            password: Password to verify

        Returns:
            The authenticated `User` if credentials match, otherwise `None`.
        """
        # Find user by email
        user = self._repository.get_by_email(email)
        if user is None:
            return None

        # Verify password using bcrypt
        try:
            stored_hash = user.password.encode("utf-8")
            if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                return None
        except Exception:
            # If stored password isn't valid bcrypt hash or verification fails
            return None

        return user

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format using basic string checks.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email is valid, False otherwise
        """
        if not email or len(email) < 5:
            return False

        if email.count("@") != 1:
            return False

        local_part, domain = email.split("@")

        if not local_part or not domain:
            return False

        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            return False

        return True
