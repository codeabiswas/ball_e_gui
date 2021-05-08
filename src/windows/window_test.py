"""
window_test.py
---
This file contains the TestWindow class, which is used for loading singular screen widgets for prototyping and testing.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow


class TestWindow(QMainWindow):
    """TestWindow.

    This class creates a frameless window around a given QWidget object.
    """
    def __init__(self, some_widget, parent=None):
        """__init__.

        Initializes the QMainWindow object with appropriate arguments

        :param some_widget: The QWidget object to be displayed
        :param parent: Default arg.
        """
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setWindowTitle(some_widget.get_window_title())
        self.setCentralWidget(some_widget)
