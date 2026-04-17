# Task Management Service

## Project Description

This project is a Python backend service for managing tasks with a clean layered architecture. It provides a foundation for task lifecycle operations while keeping the implementation minimal and framework-free for future expansion.

## Features

- Task entity defined with Python dataclasses
- In-memory task storage layer
- Layered architecture with clear separation of responsibilities
- Placeholders for API, service, repository, and domain layers

## Architecture

The project follows a layered design:

- `api`: API layer and routing placeholders
- `services`: business logic and orchestration
- `repositories`: data access and persistence abstraction
- `domain`: core task entity and models

This structure keeps the service modular and ready for future upgrades like FastAPI and database persistence.

## Project Structure

```
src/
├── api/
│   └── task_routes.py
├── domain/
│   └── task.py
├── repositories/
│   └── task_repository.py
├── services/
│   └── task_service.py
└── __init__.py

tests/
└── __init__.py
``` 

## How to Run

1. Ensure Python 3.10+ is installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies if any are added later. Currently, this project uses only the Python standard library.
4. Use the Python interpreter to inspect or import modules:
   ```bash
   python -c "from src.domain.task import Task; print(Task(id='1', title='Example'))"
   ```

> Note: The current version is a skeleton project with placeholder layers. A runnable API server will be added in a future iteration.

## Future Plans

- Add a FastAPI-based HTTP API layer
- Implement a persistent database storage option
- Add unit tests and integration tests
- Complete service and repository logic for CRUD operations
