import json
import sys
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
from Task import Task, Priority


class TaskStorage:
    def __init__(self, filename: str = "tasks_storage.json"):
        """Initialize storage with file path handling for both dev and bundled environments"""
        """Making a hidden directory for the storage file"""
        if getattr(sys, "frozen", False):
            # If the application is bundled (exe)
            # sys.executable points to the exe file
            base_path = Path(sys.executable).parent
        else:
            # If running in development
            # __file__ points to the current script file
            base_path = Path(__file__).parent

        # Create a data directory next to the executable/script
        self.storage_dir = base_path / ".data"
        self.storage_dir.mkdir(exist_ok=True)

        self.storage_path = self.storage_dir / filename

    def save_tasks(self, tasks: List[Task]) -> bool:
        """Save tasks to storage file"""
        try:
            # Convert tasks to serializable format
            task_data = [self._task_to_JSON(task) for task in tasks]

            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(task_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False

    def load_tasks(self) -> List[Task]:
        """Load tasks from storage file"""
        try:
            if not self.storage_path.exists():
                return []

            with open(self.storage_path, "r", encoding="utf-8") as f:
                task_data = json.load(f)

            return [self._JSON_to_task(data) for data in task_data]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []

    def clear_storage(self) -> bool:
        """Clear all stored tasks"""
        try:
            if self.storage_path.exists():
                self.storage_path.unlink()
            return True
        except Exception as e:
            print(f"Error clearing storage: {e}")
            return False

    def get_storage_info(self) -> Dict[str, Any]:
        """Get information about the storage"""
        return {
            "storage_location": str(self.storage_path),
            "exists": self.storage_path.exists(),
            "size_bytes": (
                self.storage_path.stat().st_size if self.storage_path.exists() else 0
            ),
            "last_modified": (
                datetime.fromtimestamp(self.storage_path.stat().st_mtime).isoformat()
                if self.storage_path.exists()
                else None
            ),
        }

    # Private helper functions

    def _task_to_JSON(self, task: Task) -> Dict[str, Any]:
        """Convert Task object to dictionary for JSON serialization"""
        task_dict = {
            "name": task.name,
            "status": task.status,
        }

        # Handle optional fields with special serialization
        if task.description:
            task_dict["description"] = task.description

        if task.deadline:
            task_dict["deadline"] = task.deadline.isoformat()

        if task.priority:
            task_dict["priority"] = task.priority.value

        if task.workload:
            task_dict["workload"] = task.workload

        return task_dict

    def _JSON_to_task(self, data: Dict[str, Any]) -> Task:
        """Convert dictionary to Task object"""
        # Handle optional fields with special deserialization
        if "deescription" in data and data["description"]:
            description = data["description"]
        else:
            description = None

        if "deadline" in data and data["deadline"]:
            deadline = datetime.fromisoformat(data["deadline"])
        else:
            deadline = None

        if "priority" in data and data["priority"]:
            priority = Priority(data["priority"])
        else:
            priority = None

        if "workload" in data and data["workload"]:
            workload = data["workload"]
        else:
            workload = None

        # Create task instance
        task = Task(
            name=data["name"],
            description=description,
            deadline=deadline,
            priority=priority,
            workload=workload,
        )

        # Set status after creation
        if data.get("status", False):
            task.mark_complete()
        else:
            task.mark_incomplete()

        return task
