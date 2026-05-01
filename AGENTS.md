# AGENTS.md

## Project Overview
- This project is a Task Management Service implemented as a Python backend.
- The service is designed to manage tasks with CRUD operations in a layered architecture.
- Data is currently stored in-memory, with future plans to integrate a database.

## Technology Stack
- Language: Python
- Architecture: Layered (api → services → repositories → domain)
- Runtime: Python standard library for the current skeleton

## Architectural Rules
- Follow strict separation of concerns:
  - `api`: placeholder for HTTP and request/response routing
  - `services`: contains business logic and orchestration
- `repositories`: handles data access and storage abstraction
    - Repositories should define clear interfaces for data access.
    - Implementation details (e.g., in-memory, database) should be interchangeable.  - `domain`: defines core task models and entities
- Do not mix responsibilities between layers.
- Use Python dataclasses for domain models.
- Keep modules focused and minimal.
- Domain models should be simple and mostly immutable.
- Business validation should not be placed inside domain models; it belongs to the service layer.

## Coding Guidelines
- Write clean, readable, and idiomatic Python code.
- Avoid unnecessary complexity.
- Use descriptive names for classes, functions, and variables.
- Prefer type hints for public interfaces.
- Keep implementation minimal until business logic is required.

## Constraints for AI Agents
- Do not introduce new architectural patterns without explicit instruction.
- Do not modify project structure unless required.
- Always follow the existing layered architecture.
- Do not add frameworks or external dependencies before explicit instruction.

## Context Usage Rule
- Always refer to the `/docs` folder for detailed project context, planning, and decision-making before implementing any feature.