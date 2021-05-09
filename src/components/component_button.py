"""
component_button.py
---
This file contains various classes required to configure various types of buttons used throughout the GUI app for Ball-E.
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
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    from PyQt5.QtWidgets import QPushButton, QSizePolicy


class GenericButton(QPushButton):
    """GenericButton.

    This class configures a Generic QPushButton that is used for most of the GUI for easy visibility and 'clickability'
    """

    def __init__(self, button_title):
        """__init__.

        Configures the QPushButton object as designed

        :param button_title: String which contains the text that must be displayed in this object
        """
        super().__init__()
        # Set the text of this QPushButton
        self.setText(button_title)
        # Keep the width policy default but set the height to be as big as possible
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        # Set a limit to how big the height can be
        self.setMaximumHeight(int(sc.FONT_XL[:2]))

        # Use CSS to set the font-size of this button
        self.setStyleSheet(
            """
            font-size: {font_size};
            """.format(font_size=sc.FONT_L)
        )


class FullPageButton(QPushButton):
    """FullPageButton.

    This class configures a Full Page QPushButton that is used for screens of the GUI that only consist of buttons
    """

    def __init__(self, button_title):
        """__init__.

        Configures the QPushButton object as designed

        :param button_title: String which contains the text that must be displayed in this object
        """

        super().__init__()
        # Set the text of this QPushButton
        self.setText(button_title)
        # Keep the width policy default but set the height to be as big as possible
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        # Use CSS to set the font-size of this button
        self.setStyleSheet(
            """
            font-size: {font_size};
            """.format(font_size=sc.FONT_L)
        )


class ProfileCreateButton(QPushButton):
    """ProfileCreateButton.

    This class configures a QPushButton used for Profile Creation
    """

    def __init__(self):
        """__init__.

        Configures the QPushButton object as designed
        """

        super().__init__()
        # Set the text of this QPushButton
        self.setText("Create New")
        # Set a fixed width for the button
        self.setFixedWidth(150)
        # Use CSS to set the background color, font color, font size, and font weight of this button
        self.setStyleSheet(
            """
            background-color: green;
            color: white;
            font-size: {font_size};
            font-weight: bold;
            """.format(font_size=sc.FONT_M)
        )


class ProfileDeleteButton(QPushButton):
    """ProfileDeleteButton.

    This class configures a QPushButton used for Profile Deletion
    """

    def __init__(self):
        """__init__.

        Configures the QPushButton object as designed
        """

        super().__init__()
        # Set the text of this QPushButton
        self.setText("Delete")
        # Keep the width fixed but make its height as big as possible
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )
        # Fix the width
        self.setFixedWidth(100)
        # Use CSS to set the background color, font color, font size, and font weight of this button
        self.setStyleSheet(
            """
            background-color: red;
            color: white;
            font-size: {font_size};
            font-weight: bold;
            """.format(font_size=sc.FONT_S)
        )
