from datetime import date
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

try:
    from pydantic import ConfigDict
except ImportError:  # Pydantic v1 compatibility
    ConfigDict = None

from src.domain.task import Task
from src.domain.task_status import TaskStatus
from src.repositories.task_repository import InMemoryTaskRepository
from src.services.task_service import TaskService, TaskValidationError

router = APIRouter()

task_service = TaskService(InMemoryTaskRepository())


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    description: Optional[str] = None
    priority: str = "normal"
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    user_id: str
    description: Optional[str] = None
    status: TaskStatus
    priority: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    if ConfigDict is not None:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(request: TaskCreateRequest):
    try:
        task = task_service.create(
            title=request.title,
            user_id=request.user_id,
            description=request.description,
            priority=request.priority,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        return task
    except TaskValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=List[TaskResponse])
def get_tasks(user_id: str = Query(..., description="User ID to filter tasks")):
    return task_service.get_all(user_id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, user_id: str = Query(..., description="User ID for task ownership check")):
    task = task_service.get_by_id(task_id, user_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    request: TaskUpdateRequest,
    user_id: str = Query(..., description="User ID for task ownership check"),
):
    existing_task = task_service.get_by_id(task_id, user_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        updated_task = Task(
            id=task_id,
            title=request.title if request.title is not None else existing_task.title,
            user_id=existing_task.user_id,
            description=request.description,
            status=request.status,
            priority=request.priority if request.priority is not None else existing_task.priority,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        result = task_service.update(updated_task)
        if result is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return result
    except TaskValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{task_id}")
def delete_task(task_id: str, user_id: str = Query(..., description="User ID for task ownership check")):
    # Ensure the task belongs to the requesting user
    existing = task_service.get_by_id(task_id, user_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    deleted = task_service.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
