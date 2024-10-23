from typing import List, Optional
from datetime import date
from enum import Enum
from Task import Task, Priority

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    # Task related methods

    def create_task(
        self,
        name: str,
        description: Optional[str] = None,
        deadline: Optional[date] = None,
        priority: Optional[Priority] = None,
        story_points: Optional[int] = None
    ) -> Task:
        """Create a new task and add it to the task list"""
        task = Task(name, description, deadline, priority, story_points)
        self.tasks.append(task)
        return task
    
    def add_task(self, task: Task) -> None:
        """Add a task to the list"""
        self.tasks.append(task)

    def get_task_by_index(self, index: int) -> Optional[Task]:
        """Get a specific task by index"""
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None

    def remove_task(self, index: int) -> bool:
        """Remove a specific task from the list"""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            return True
        return False

    def remove_all_tasks(self) -> None:
        """Remove all tasks from the list"""
        self.tasks.clear()

    def update_task(
        self,
        index: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[date] = None,
        priority: Optional[Priority] = None,
        story_points: Optional[int] = None
    ) -> bool:
        """Update task attributes if provided"""
        task = self.get_task_by_index(index)
        if task is None:
            return False
        
        if name is not None:
            task.name = name
        if description is not None:
            task.description = description
        if deadline is not None:
            task.deadline = deadline
        if priority is not None:
            task.priority = priority
        if story_points is not None:
            task.story_points = story_points
        
        return True

    def complete_task(self, index: int) -> bool:
        """Mark a specific task as complete"""
        task = self.get_task_by_index(index)
        if task is None:
            return False
        task.mark_complete()
        return True

    # Sorting methods

    def sort_by_name(self, reverse: bool = False) -> List[Task]:
        """Sort tasks by name"""
        return sorted(self.tasks, key=lambda x: x.name, reverse=reverse)
    
    def sort_by_status(self, reverse: bool = False) -> List[Task]:
        """Sort tasks by completion status"""
        return sorted(self.tasks, key=lambda x: x.status, reverse=reverse)

    def sort_by_deadline(self, reverse: bool = False) -> List[Task]:
        """Sort tasks by deadline (None values at the end)"""
        return sorted(
            self.tasks,
            key=lambda x: (x.deadline is None, x.deadline or date.max),
            reverse=reverse
        )

    def sort_by_priority(self, reverse: bool = False) -> List[Task]:
        """Sort tasks by priority (None values at the end)"""
        priority_order = {
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
            None: 4
        }
        return sorted(
            self.tasks,
            key=lambda x: priority_order[x.priority],
            reverse=reverse
        )

    # Filtering methods
    
    def filter_by_name(self, keyword: str) -> List[Task]:
        """Filter tasks by name containing keyword"""
        return [task for task in self.tasks if keyword.lower() in task.name.lower()]

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Filter tasks by completion status"""
        return [task for task in self.tasks if task.status == completed]

    def filter_by_deadline_range(self, start_date: date, end_date: date) -> List[Task]:
        """Filter tasks by deadline range"""
        return [
            task for task in self.tasks
            if task.deadline and start_date <= task.deadline <= end_date
        ]
    
    def filter_by_priority(self, priority: Priority) -> List[Task]:
        """Filter tasks by priority"""
        return [task for task in self.tasks if task.priority == priority]

    # Other utility methods

    def get_overdue_tasks(self) -> List[Task]:
        """Get all tasks that are past their deadline and not completed"""
        today = date.today()
        return [
            task for task in self.tasks
            if task.deadline and task.deadline < today and not task.status
        ]
    
    def num_of_tasks(self) -> int:
        """Return number of tasks"""
        return len(self.tasks)

    def __str__(self) -> str:
        """String representation of all tasks"""
        if not self.tasks:
            return "No tasks available"
        return "\n".join(str(task) for task in self.tasks)

