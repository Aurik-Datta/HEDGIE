import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore

class DesktopPet(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Load and resize pet image
        self.pixmap = QtGui.QPixmap("pet.png")  # Replace with your image path
        self.pixmap = self.pixmap.scaled(378, 378, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.pixmap)
        self.resize(self.pixmap.size())

        # Get screen geometry
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        available_geometry = QtWidgets.QDesktopWidget().availableGeometry()

        # Set initial position above the taskbar
        self.move(10, available_geometry.height() - self.height())

        # Initialize movement variables
        self.x_velocity = random.choice([-2, -1, 1, 2])
        self.y_velocity = random.choice([-2, -1, 1, 2])

        # Movement control flags
        self.movement_mode = 'automatic'  # Default movement mode
        self.is_paused = False  # Flag to pause movement

        # Start the timer for continuous movement
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move_pet)
        self.timer.start(50)  # Update every 50 ms

        # Create context menu
        self.context_menu = QtWidgets.QMenu(self)
        automatic_action = self.context_menu.addAction("Automatic Movement")
        automatic_action.triggered.connect(self.set_automatic_movement)
        manual_action = self.context_menu.addAction("Manual Movement")
        manual_action.triggered.connect(self.set_manual_movement)
        quit_action = self.context_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_pet)

        # Start mouse listener
        # self.listener = mouse.Listener(on_click=self.on_click)
        # self.listener.start()  # Start the listener

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.is_paused = True  # Pause movement
            self.context_menu.exec_(event.globalPos())  # Show context menu at mouse position
            self.is_paused = False  # Resume movement after the menu is closed

    def move_pet(self):
        if self.movement_mode == 'automatic' and not self.is_paused:
            # Update the position of the pet automatically
            current_x = self.x()
            current_y = self.y()

            # Move the pet
            new_x = current_x + self.x_velocity
            new_y = current_y + self.y_velocity

            # Bounce off the edges of the screen
            screen_width = self.screen().geometry().width()
            screen_height = self.screen().geometry().height()

            if new_x < 0 or new_x > (screen_width - self.width()):
                self.x_velocity = -self.x_velocity
            if new_y < 0 or new_y > (screen_height - self.height()):
                self.y_velocity = -self.y_velocity

            # Set the new position
            self.move(new_x, new_y)

    def set_automatic_movement(self):
        self.movement_mode = 'automatic'

    def set_manual_movement(self):
        self.movement_mode = 'manual'

    def quit_pet(self):
        QtWidgets.QApplication.quit()  # Quit the application

# Main application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()  # Show the pet

    sys.exit(app.exec_())
