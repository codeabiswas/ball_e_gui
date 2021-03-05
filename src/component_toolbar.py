import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QHBoxLayout, QLabel,
                             QLayout, QMainWindow, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)


class ToolbarButton(QPushButton):
    def __init__(self, button_title):
        super().__init__()
        self.setText(button_title)
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )
        screen_info = QDesktopWidget().screenGeometry(0)
        self.setFixedWidth(int(0.25*screen_info.width()))

        self.setStyleSheet(
            """
            font-size: 24px;
            background-color: white
            """
        )

class ToolbarTitle(QLabel):
    def __init__(self, toolbar_title):
        super().__init__()
        self.setText(toolbar_title)
        self.setStyleSheet(
            """
            color: white;
            font-size: 60px;
            font-weight: bold
            """
        )
        self.setAlignment(Qt.AlignCenter)

class ToolbarComponent(QWidget):
    def __init__(self, screen_title, prev_screen_button_title="", parent=None):
        super().__init__(parent=parent)

        self.setStyleSheet(
            """
            background-color: #2E75B6
            """
        )

        screen_info = QDesktopWidget().screenGeometry(0)
        self.setFixedHeight(int(0.05*screen_info.width()))

        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.setContentsMargins(0,0,0,0)

        if prev_screen_button_title != "":
            self.prev_screen_button = ToolbarButton(prev_screen_button_title)
            self.toolbar_layout.addWidget(self.prev_screen_button)

        self.screen_title_label = ToolbarTitle(screen_title)
        self.toolbar_layout.addWidget(self.screen_title_label)

        self.back_to_home_button = ToolbarButton("Back to Home")
        self.toolbar_layout.addWidget(self.back_to_home_button)

        self.setLayout(self.toolbar_layout)
