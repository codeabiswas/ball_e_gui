import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from component_button import Button
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class ProfilesScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Profiles"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        button_layout = QHBoxLayout()
        self.goalie_profiles_button = Button("Goalie Profiles")
        self.drill_profiles_button = Button("Drill Profiles")
        button_layout.addWidget(self.goalie_profiles_button)
        button_layout.addWidget(self.drill_profiles_button)

        screen_layout.addLayout(button_layout)

        self.setLayout(screen_layout)

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(ProfilesScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
