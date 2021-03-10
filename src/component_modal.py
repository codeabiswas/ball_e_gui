from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDesktopWidget, QDialog, QHBoxLayout, QLabel,
                             QVBoxLayout, QWidget)

import style_constants as sc


class Modal(QDialog):

    def __init__(self, type, layout, window_title):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle(window_title)

        modal_layout = QVBoxLayout()
        heading_bar = QWidget()
        heading_bar_layout = QHBoxLayout()
        heading_bar.setFixedHeight(int(0.03*sc.SCREEN_WIDTH))

        heading_bar_label = QLabel()

        heading_bar_label.setAlignment(Qt.AlignCenter)
        heading_bar_label.setStyleSheet(
            """
            font-size: {font_size};
            color: white;
            """.format(font_size=sc.FONT_L)
        )
        heading_bar_layout.addWidget(heading_bar_label)

        if type == "info":
            heading_bar.setStyleSheet(
                """
                background-color: {background_color};
                """.format(background_color=sc.COLOR_INFO)
            )
            heading_bar_label.setText("Info: {}".format(window_title))
        elif type == "error":

            heading_bar.setStyleSheet(
                """
                background-color: {background_color};
                """.format(background_color=sc.COLOR_ERROR)
            )
            heading_bar_label.setText("Error: {}".format(window_title))

        else:
            raise Exception("{} is not a valid modal type.".format(type))

        heading_bar.setLayout(heading_bar_layout)

        modal_layout.addWidget(heading_bar)

        modal_layout.addLayout(layout)
        self.setLayout(modal_layout)
        self.exec_()
