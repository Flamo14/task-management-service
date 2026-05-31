from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.services.user_service import UserService, UserRegistrationError
from src.repositories.user_repository import InMemoryUserRepository


router = APIRouter()

user_service = UserService(InMemoryUserRepository())


class UserRegisterRequest(BaseModel):
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=1)


class UserAuthRequest(BaseModel):
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: str
    email: str


@router.post("/register", response_model=UserResponse, status_code=201)
def register(request: UserRegisterRequest):
    try:
        user = user_service.register(request.email, request.password)
        return UserResponse(id=user.id, email=user.email)
    except UserRegistrationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=Optional[UserResponse])
def login(request: UserAuthRequest):
    user = user_service.authenticate(request.email, request.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return UserResponse(id=user.id, email=user.email)
