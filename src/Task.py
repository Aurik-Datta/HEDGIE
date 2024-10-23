from enum import Enum
from datetime import date
from typing import Optional

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        deadline: Optional[date] = None,
        priority: Optional[Priority] = None,
        story_points: Optional[int] = None
    ):
        self.name = name
        self.status = False
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.story_points = story_points

    def mark_complete(self) -> None:
        """Mark the task as complete"""
        self.status = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete"""
        self.status = False

    def __str__(self) -> str:
        status_str = "Complete" if self.status else "Incomplete"
        priority_str = f", Priority: {self.priority.value}" if self.priority else ""
        deadline_str = f", Deadline: {self.deadline}" if self.deadline else ""
        points_str = f", Points: {self.story_points}" if self.story_points else ""
        
        return f"Task: {self.name} - Status: {status_str}{priority_str}{deadline_str}{points_str}"
