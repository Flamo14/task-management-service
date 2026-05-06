### Mermaid
flowchart TD
    A[Start] --> B{Is title valid?}
    B -- No --> C[Return validation error]
    B -- Yes --> D{Is user_id valid?}
    D -- No --> E[Return validation error]
    D -- Yes --> F[Assign task id]
    F --> G[Set default status = pending]
    G --> H[Return created task]
