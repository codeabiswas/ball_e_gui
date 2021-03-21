import sys
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QLabel, QMainWindow,
                             QPushButton, QScrollArea, QSizePolicy,
                             QVBoxLayout, QWidget)

from component_button import GenericButton
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class HelpScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Help"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        self.calibration_screen_button = GenericButton("Calibration")
        self.training_screen_button = GenericButton("Training")
        self.profiles_screen_button = GenericButton("Profiles")
        self.session_recording_screen_button = GenericButton(
            "Session Recording")

        screen_layout.addWidget(self.calibration_screen_button)
        screen_layout.addWidget(self.training_screen_button)
        screen_layout.addWidget(self.profiles_screen_button)
        screen_layout.addWidget(self.session_recording_screen_button)

        self.setLayout(screen_layout)

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(HelpScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
