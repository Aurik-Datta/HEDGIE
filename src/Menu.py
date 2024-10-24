from PyQt5 import QtWidgets
import sys
from TaskManager import TaskManager


# Menu class that holds the task management window
class Menu(QtWidgets.QWidget):
    def __init__(self, task_manager: TaskManager):
        super().__init__()
        self.task_manager = task_manager
        self.create_ui()

    def create_ui(self):
        # Create layout (canvas that holds widgets)
        self.layout = QtWidgets.QVBoxLayout()

        # Create list widget to display tasks
        self.task_list = QtWidgets.QListWidget()

        # Create buttons
        self.create_button = QtWidgets.QPushButton("Create Task")
        self.update_button = QtWidgets.QPushButton("Update Task")
        self.delete_button = QtWidgets.QPushButton("Delete Task")

        # Add list and buttons to layout and set the layout to the main window
        self.layout.addWidget(self.task_list)
        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)
        self.setWindowTitle("Task Manager")
        self.update_task_list()

    # Helper function to update the task list on any action
    def update_task_list(self):
        self.task_list.clear()
        for task in self.task_manager.sort_by_deadline():
            self.task_list.addItem(task.name)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    task_manager = TaskManager()
    print(task_manager)

    menu = Menu(task_manager)
    menu.show()
    sys.exit(app.exec_())
