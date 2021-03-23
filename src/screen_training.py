import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)

from component_button import GenericButton
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class TrainingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Training Screen"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        button_layout = QHBoxLayout()

        self.load_goalie_profile_button = GenericButton("Load Goalie Profile")
        self.load_drill_profile_button = GenericButton("Load Drill Profile")
        self.manual_session_button = GenericButton("Manual Session")

        button_layout.addWidget(self.load_goalie_profile_button)
        button_layout.addWidget(self.load_drill_profile_button)
        button_layout.addWidget(self.manual_session_button)

        screen_layout.addLayout(button_layout)

        self.setLayout(screen_layout)

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
