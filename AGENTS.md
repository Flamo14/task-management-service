# AGENTS.md

## Project Overview
- This project is a Task Management Service implemented as a REST API.
- The service allows users to create, read, update, and delete tasks.
- Data is currently stored in-memory, with future plans to integrate a database.

## Technology Stack
- Language: Scala
- Architecture: Layered (routes → service → repository)
- Build tool: sbt

## Architectural Rules
- Follow strict separation of concerns:
  - routes: handle HTTP and request/response mapping only
  - service: contains business logic
  - repository: handles data storage
- Do not mix responsibilities between layers.
- Use case classes for domain models.
- Prefer immutable data structures.

## Coding Guidelines
- Write clean, readable, and idiomatic Scala code.
- Avoid unnecessary complexity.
- Use descriptive names for variables and functions.

## Constraints for AI Agents
- Do not introduce new architectural patterns without explicit instruction.
- Do not modify project structure unless required.
- Always follow the existing layered architecture.

## Context Usage Rule
- Always refer to the `/docs` folder for detailed project context, planning, and decision-making before implementing any feature.