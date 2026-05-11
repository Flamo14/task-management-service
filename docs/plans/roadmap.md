# Roadmap (MVP)

## MVP Scope

The initial version of the system includes:
- Create a task
- Retrieve all tasks
- Update a task
- Delete a task

Data is currently stored in-memory.

---

# Current Status

Current Stage:
Stage 2 — Core Functionality

Completed:
- Project structure
- Layered architecture
- Task domain model
- User domain model
- In-memory repositories
- Task CRUD operations
- User registration
- Task ownership (user_id)
- Task status validation
- Basic business validation

In Progress:
- AI-generated architecture experiments
- Pure function experiment
- Design pattern implementation

Next Steps:
- API layer
- Authentication
- Database integration

---

## Stage 1: Project Setup COMPLETE
- Define project structure
- Implement basic models
- Set up repository layer

---

## Stage 2: Core Functionality COMPLETE
- Implement service layer logic
- Add CRUD operations
- Ensure proper separation of concerns
- Add validation
- Add task ownership
- Add task status handling

---

## Stage 3: API Layer IN PROGRESS
- Implement REST endpoints
- Connect routes to service layer
- Handle request/response mapping

---

## Stage 4: Improvements PLANNED
- Improve error handling
- Refactor code
- Add tests

---

## Future Enhancements
- PostgreSQL integration
- Authentication and authorization
- Filtering and pagination
- Streamlit UI