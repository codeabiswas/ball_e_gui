import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)

from window_test import TestWindow


class TrainingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window_title = "Training Screen"

        dummy_layout = QVBoxLayout()

        dummy_layout.addWidget(QLabel("Training Screen"))

        self.home_button = QPushButton('Back to Home')
        dummy_layout.addWidget(self.home_button)

        self.setLayout(dummy_layout)

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
