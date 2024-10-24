from enum import Enum
from datetime import datetime
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
        deadline: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        workload: Optional[int] = None,
    ):
        self.name = name
        self.status = False
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.workload = workload

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
        workload_str = f", Workload: {self.workload}" if self.workload else ""

        return f"Task: {self.name} - Status: {status_str}{priority_str}{deadline_str}{workload_str}"
