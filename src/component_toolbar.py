import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QHBoxLayout, QLabel,
                             QLayout, QMainWindow, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

import style_constants as sc


class ToolbarButton(QPushButton):
    def __init__(self, button_title):
        super().__init__()
        self.setText(button_title)
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )
        self.setFixedWidth(int(0.25*sc.SCREEN_WIDTH))

        self.setStyleSheet(
            """
            font-size: {font_size};
            background-color: white
            """.format(font_size=sc.FONT_L)
        )


class ToolbarTitle(QLabel):
    def __init__(self, toolbar_title):
        super().__init__()
        self.setText(toolbar_title)
        self.setStyleSheet(
            """
            color: white;
            font-size: {font_size};
            font-weight: bold
            """.format(font_size=sc.FONT_XL)
        )
        self.setAlignment(Qt.AlignCenter)


class ToolbarComponent(QWidget):
    def __init__(self, screen_title, prev_screen_button_title="", parent=None):
        super().__init__(parent=parent)

        self.setStyleSheet(
            """
            background-color: {background_color}
            """.format(background_color=sc.COLOR_TOOLBAR)
        )

        self.setFixedHeight(int(0.15*sc.SCREEN_WIDTH))

        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.setContentsMargins(0, 0, 0, 0)

        if prev_screen_button_title != "":
            self.prev_screen_button = ToolbarButton(prev_screen_button_title)
            self.toolbar_layout.addWidget(self.prev_screen_button)

        self.screen_title_label = ToolbarTitle(screen_title)
        self.toolbar_layout.addWidget(self.screen_title_label)

        self.back_to_home_button = ToolbarButton("Back to Home")
        self.toolbar_layout.addWidget(self.back_to_home_button)

        self.setLayout(self.toolbar_layout)
