# Models.py Notes

## Here’s a breakdown of each model:

### Column Model:

- id: The primary key that uniquely identifies each column.
- name: The name of the column (e.g., "To Do", "In Progress", "Done").
- tasks: A relationship to the Task model, establishing that each column can have many tasks.

### Task Model:

- id: The primary key that uniquely identifies each task.
- title: The title of the task.
- description: (Optional) A brief description of the task.
- column_id: A foreign key that links each task to a specific column.

_Note: The db.relationship and db.ForeignKey are used to establish a one-to-many relationship between Column and
Task—each column can have multiple tasks, but each task belongs to only one column._