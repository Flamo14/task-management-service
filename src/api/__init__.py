from fastapi import FastAPI

from .task_routes import router as task_router

app = FastAPI(title="Task Management Service")
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
