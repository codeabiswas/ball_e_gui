import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
                             QMainWindow, QPushButton, QSizePolicy,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

import style_constants as sc
from component_button import GenericButton
from component_labels import ProfileLabel
from component_toolbar import ToolbarComponent
from helper_profiler import Profiler
from window_test import TestWindow


class TrainingSessionCompleteScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Training Complete"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        screen_layout.addWidget(ProfileLabel(
            "Training Complete"))

        self.setLayout(screen_layout)

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingSessionCompleteScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
