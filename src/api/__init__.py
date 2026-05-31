from fastapi import FastAPI

from .task_routes import router as task_router
from .user_routes import router as user_router

app = FastAPI(title="Task Management Service")
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/users", tags=["users"])
