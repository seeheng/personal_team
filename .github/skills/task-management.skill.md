# Task Management Skill

## Skill Metadata
```yaml
name: task-management
version: 1.0.0
description: Manages tasks, todos, schedules, and reminders for the personal assistant
agent: personal-assistant
category: productivity
status: active
```

## Overview
This skill enables the personal assistant agent to:
- Create and manage tasks and todos
- Set reminders and alerts
- Organize tasks by priority and category
- Track task completion status
- Generate productivity reports

## Capabilities

### Core Features
- **Task Creation**: Add new tasks with titles, descriptions, and priorities
- **Task Organization**: Categorize tasks and group by projects
- **Priority Management**: Set and adjust task priorities (High, Medium, Low)
- **Due Dates**: Assign deadlines and track overdue tasks
- **Status Tracking**: Monitor task progress (Not Started, In Progress, Completed)
- **Reminders**: Set up automated reminders for upcoming tasks
- **Recurring Tasks**: Create repeating tasks (daily, weekly, monthly)

### Task Properties
```json
{
  "id": "task_001",
  "title": "Complete project proposal",
  "description": "Detailed description of the task",
  "category": "work",
  "priority": "high",
  "status": "in-progress",
  "due_date": "2026-03-15",
  "created_at": "2026-03-06",
  "completed_at": null,
  "tags": ["project", "important"],
  "assigned_to": "user@example.com",
  "recurring": "weekly"
}
```

## Key Methods

### Task Operations
- `create_task(title, description, priority, due_date, category)`
- `update_task(task_id, **updates)`
- `delete_task(task_id)`
- `complete_task(task_id)`
- `list_tasks(filter_by, sort_by)`
- `get_task(task_id)`

### Organization
- `create_category(name, description)`
- `add_tag(task_id, tag)`
- `filter_by_priority(priority)`
- `filter_by_status(status)`
- `filter_by_due_date(start_date, end_date)`

### Reminders
- `set_reminder(task_id, remind_at, notification_type)`
- `get_active_reminders()`
- `dismiss_reminder(reminder_id)`
- `snooze_reminder(reminder_id, duration)`

### Analytics
- `get_task_statistics()`
- `get_completion_rate()`
- `get_overdue_tasks()`
- `generate_report(start_date, end_date)`

## Integration Examples

### Usage in Agent
```python
# Create a task
task = agent.use_skill("task-management", "create_task", {
    "title": "Review handwriting recognition results",
    "description": "Check OCR accuracy on test samples",
    "priority": "high",
    "due_date": "2026-03-10",
    "category": "development"
})

# List all high-priority tasks
high_priority = agent.use_skill("task-management", "list_tasks", {
    "filter_by": "priority",
    "value": "high"
})

# Mark task as complete
agent.use_skill("task-management", "complete_task", {
    "task_id": task['id']
})

# Set reminder
agent.use_skill("task-management", "set_reminder", {
    "task_id": task['id'],
    "remind_at": "2026-03-09 09:00:00",
    "notification_type": "email"
})
```

## Data Storage
Tasks are stored in JSON format for easy access and persistence:
```
./data/tasks/
├── active_tasks.json
├── completed_tasks.json
└── categories.json
```

## Notifications
- **Email**: Email notifications for task reminders
- **Desktop**: System notifications for urgent tasks
- **SMS**: Optional SMS reminders for critical tasks
- **Calendar Sync**: Integration with calendar applications

---

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: March 6, 2026
