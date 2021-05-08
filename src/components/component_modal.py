"""
component_modal.py
---
This file contains the Modal object that is used throughout Ball-E's GUI app.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

try:
    import pathlib
    import sys
    sys.path.append(
        "{}/Developer/ball_e_gui/src/helpers".format(pathlib.Path.home()))

    import style_constants as sc

    from component_button import GenericButton
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QLabel, QVBoxLayout,
                                 QWidget)


class Modal(QDialog):
    """Modal.

    This class configures the QDialog object that is used throughout the GUI as the main modal object.
    """


    def __init__(self, type, layout, window_title):
        """__init__.

        Configures the QDialog object as designed
        :param type: The type of QDialog to be shown
        :param layout: Sets whatever content within the modal
        :param window_title: Sets the title of the modal window
        """
        super().__init__()

        # Flags to make it look like the designed modal and ensure it always stays on top regardless of where the user clicks
        self.setWindowFlags(Qt.WindowStaysOnTopHint |
                            Qt.WindowCloseButtonHint | Qt.FramelessWindowHint)
        self.setWindowTitle(window_title)

        # Customize the modal
        modal_layout = QVBoxLayout()
        heading_bar = QWidget()
        heading_bar_layout = QHBoxLayout()
        # heading_bar.setFixedHeight(int(0.03*sc.SCREEN_WIDTH))
        heading_bar.setMinimumHeight(int(0.05*sc.SCREEN_WIDTH))

        heading_bar_label = QLabel()

        heading_bar_label.setAlignment(Qt.AlignCenter)
        heading_bar_label.setStyleSheet(
            """
            font-size: {font_size};
            color: white;
            """.format(font_size=sc.FONT_XL)
        )
        heading_bar_layout.addWidget(heading_bar_label)

        # Depending on the type of modal, customize it appropriately
        if type == "info":
            heading_bar.setStyleSheet(
                """
                background-color: {background_color};
                """.format(background_color=sc.COLOR_INFO)
            )
            heading_bar_label.setText(window_title)
        elif type == "error":

            heading_bar.setStyleSheet(
                """
                background-color: {background_color};
                """.format(background_color=sc.COLOR_ERROR)
            )
            heading_bar_label.setText(window_title)

        elif type == "choice":
            heading_bar.setStyleSheet(
                """
                background-color: {background_color};
                """.format(background_color=sc.COLOR_INFO)
            )
            heading_bar_label.setText(window_title)

            self.yes_button = GenericButton("Yes")
            no_button = GenericButton("No")
            decision_buttons_layout = QHBoxLayout()
            decision_buttons_layout.addWidget(self.yes_button)
            decision_buttons_layout.addWidget(no_button)
            no_button.clicked.connect(lambda: self.close())

        else:
            raise Exception("{} is not a valid modal type.".format(type))

        heading_bar.setLayout(heading_bar_layout)

        modal_layout.addWidget(heading_bar)

        # Some extra steps if the modal's type is "choice"
        if type == "choice":
            modal_layout.addLayout(layout)
            modal_layout.addLayout(decision_buttons_layout)
        # Otherwise, for all types, follow these rules for closing
        else:
            modal_layout.addLayout(layout)
            close_modal_button = GenericButton("Close")
            close_modal_button.clicked.connect(lambda: self.close())
            modal_layout.addWidget(close_modal_button)

        self.setLayout(modal_layout)
        self.setMinimumWidth(int(0.5*sc.SCREEN_WIDTH))
        self.setMinimumHeight(int(0.5*sc.SCREEN_HEIGHT))

        # As long as the modal is not a "choice" type, execute independently
        if not type == "choice":
            self.exec_()
