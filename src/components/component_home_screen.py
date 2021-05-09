"""
component_home_screen.py
---
This file contains all the visual components designed for the Home Screen for Ball-E's GUI app.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

from PyQt5.QtWidgets import QLabel, QPushButton, QSizePolicy


class HomeScreenButton(QPushButton):
    """HomeScreenButton.

    This class configures the buttons used to denote the various locations that the user can navigate to in the home screen
    """

    def __init__(self, button_text):
        """__init__.

        Configures the QPushButton object as designed

        :param button_text: String which contains the text that must be displayed in this object
        """

        super().__init__()
        # Set the text of this QPushButton
        self.button_text = button_text
        # Keep the width policy default but set the height to be as big as possible
        self.setText(self.button_text)
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )
        # Use CSS to style the background color, font color, font size, and font wieght of this button
        self.setStyleSheet(
            """
            background-color: green;
            color: white;
            font-size: 60px;
            font-weight: bold;
            """
        )


class PowerOffButton(QPushButton):
    """PowerOffButton.

    This class configures the Power-Off button in the home screen
    """

    def __init__(self, button_text):
        """__init__.

        Configures the QPushButton object as designed

        :param button_text: String which contains the text that must be displayed in this object
        """

        super().__init__()

        # Set the text of this QPushButton
        self.button_text = button_text
        self.setText(self.button_text)
        # Set the size and shape to be a pretty large square
        self.setFixedHeight(400)
        self.setFixedWidth(400)
        # Use CSS to style the background color, font color, font size, and font weight of this button
        self.setStyleSheet(
            """
            background-color: red;
            color: white;
            font-size: 40px;
            font-weight: bold;
            """
        )


class HomeScreenTitle(QLabel):
    """HomeScreenTitle.

    This class configures the title of the GUI shown on the home screen
    """

    def __init__(self, text):
        """__init__.

        Configures the QLabel object as designed

        :param text: String which contains the text that must be displayed in this object
        """

        super().__init__()

        # Set the text of this QLabel
        self.setText(text)
        # Use CSS to style the font color, font size, and font weight of this QLabel
        self.setStyleSheet(
            """
            color: black;
            font-size: 100px;
            font-weight: bold
            """
        )


class HomeScreenSubtitle(QLabel):
    """HomeScreenSubtitle.

    This class configures the subtitle of the GUI shown on the home screen
    """

    def __init__(self, text):
        """__init__.

        Configures the QLabel object as designed

        :param text: String which contains the text that must be displayed in this object
        """

        super().__init__()
        # Set the text of this QLabel
        self.setText(text)
        # Use CSS to style the font color and font size of this QLabel
        self.setStyleSheet(
            """
            color: black;
            font-size: 60px;
            """
        )
