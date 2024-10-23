from PyQt5 import QtWidgets
import sys

# todo use fully implemented task and task manager classes
# Sample task
class Task:
    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status

# Sample task manager
class TaskManager:
    def __init__(self):
        self.tasks = []

    def create_task(self, name, description, status):
        self.tasks.append(Task(name, description, status))

    def update_task(self, index, name=None, description=None, status=None):
        if 0 <= index < len(self.tasks):
            if name is not None:
                self.tasks[index].name = name
            if description is not None:
                self.tasks[index].description = description
            if status is not None:
                self.tasks[index].status = status

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

# Menu class that holds the task management window
class Menu(QtWidgets.QWidget):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.create_ui()

    def create_ui(self):
        # Create layout (canvas that holds widgets)
        self.layout = QtWidgets.QVBoxLayout()

        # Create list widget to display tasks
        self.task_list = QtWidgets.QListWidget()
        
        # Create buttons
        self.create_button = QtWidgets.QPushButton('Create Task')
        self.update_button = QtWidgets.QPushButton('Update Task')
        self.delete_button = QtWidgets.QPushButton('Delete Task')

        # Add list and buttons to layout and set the layout to the main window
        self.layout.addWidget(self.task_list)
        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)
        self.setWindowTitle('Task Manager')
        self.update_task_list()


    # Helper function to update the task list on any action
    def update_task_list(self):
        self.task_list.clear()
        for task in self.task_manager.tasks:
            self.task_list.addItem(task.name)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    task_manager = TaskManager()
    task_manager.create_task('task', 'desc', 'compl')
    menu = Menu(task_manager)
    menu.show()
    sys.exit(app.exec_())
