# Task Management Service

## Project Description

A REST API for managing tasks, built with Scala and Akka HTTP. This service allows users to create, read, update, and delete tasks through HTTP endpoints.

## Features

- Create new tasks with title, description, and status
- Retrieve all tasks
- Get a specific task by ID
- Update existing tasks
- Delete tasks
- In-memory storage (no persistence)

## Tech Stack

- **Language**: Scala 2.13.12
- **HTTP Framework**: Akka HTTP 10.5.0
- **JSON Marshalling**: Spray JSON
- **Build Tool**: SBT

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | Retrieve all tasks |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/{id}` | Get a specific task by ID |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |

### Request/Response Examples

#### Create Task (POST /tasks)
```json
{
  "title": "Complete project",
  "description": "Finish the Scala REST API project",
  "status": "in-progress"
}
```

#### Response
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the Scala REST API project",
  "status": "in-progress"
}
```

## How to Run

1. **Prerequisites**: Ensure you have Java 8+ and SBT installed on your system.

2. **Clone or navigate to the project directory**.

3. **Install dependencies**:
   ```
   sbt update
   ```

4. **Run the application**:
   ```
   sbt run
   ```

5. The server will start on `http://localhost:8080`. You can test the endpoints using tools like curl, Postman, or any HTTP client.

## Project Structure

```
src/main/scala/
├── Main.scala              # Application entry point
├── model/
│   └── Task.scala          # Task domain model
├── repository/
│   └── TaskRepository.scala # Data access layer
├── service/
│   └── TaskService.scala   # Business logic layer
└── routes/
    └── TaskRoutes.scala    # HTTP route definitions
```