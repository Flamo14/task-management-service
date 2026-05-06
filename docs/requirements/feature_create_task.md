### User Story:
As a user,
I want to create a task,
so that I can manage my work.

### Acceptance Criteria (BDD)
Given a valid task title and user_id
When the user creates a task
Then the system should return a task with a unique id and default status "pending"

Given an empty task title
When the user tries to create a task
Then the system should return a validation error