"""
component_toolbar.py
---
This file contains the various classes required to configure the Toolbar for the GUI app for Ball-E.
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
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                                 QWidget)


class ToolbarButton(QPushButton):
    """ToolbarButton.

    This class configures and customizes the QPushButton object used in the toolbar.
    """

    def __init__(self, button_title):
        """__init__.

        Configures the QPushButton as designed.

        :param button_title: String which shows the text that the button should include
        """
        super().__init__()
        # Set the text of the button
        self.setText(button_title)
        # Keep the width fixed but make its height as big as possible
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )
        # Fix the width
        self.setFixedWidth(int(0.25*sc.SCREEN_WIDTH))

        # Use CSS to set font size and color of this button
        self.setStyleSheet(
            """
            font-size: {font_size};
            background-color: white
            """.format(font_size=sc.FONT_L)
        )


class ToolbarTitle(QLabel):
    """ToolbarTitle.

    This class configures and customizes the QLabel object used in the toolbar
    """

    def __init__(self, toolbar_title):
        """__init__.

        Configures the QLabel as designed

        :param toolbar_title: String which shows the text for the label
        """

        super().__init__()
        # Set the text of the toolbar
        self.setText(toolbar_title)
        # Use CSS to set the color, font-size, and font-weight of this label
        self.setStyleSheet(
            """
            color: white;
            font-size: {font_size};
            font-weight: bold
            """.format(font_size=sc.FONT_XL)
        )
        # Center align text in the label
        self.setAlignment(Qt.AlignCenter)


class ToolbarComponent(QWidget):
    """ToolbarComponent.

    This class combines ToolbarButton and ToolbarTitle to create a complete ToolbarComponent, which is used in most screen widgets throughout Ball-E's GUI
    """

    def __init__(self, screen_title, prev_screen_button_title="", parent=None):
        """__init__.

        Initializes a QWidget object given the parameters

        :param screen_title: String containing the title of the widget
        :param prev_screen_button_title: Optional parameter containing the string for the previous button's title
        :param parent: Default arg.
        """

        super().__init__(parent=parent)

        # Use CSS to set the background color of the widget
        self.setStyleSheet(
            """
            background-color: {background_color}
            """.format(background_color=sc.COLOR_TOOLBAR)
        )

        # Set fixed height for the toolbar component
        self.setFixedHeight(int(0.15*sc.SCREEN_WIDTH))

        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.setContentsMargins(0, 0, 0, 0)

        # If the previous screen button title is not empty, then create a new toolbar button pertaining to the previous screen
        if prev_screen_button_title != "":
            self.prev_screen_button = ToolbarButton(prev_screen_button_title)
            self.toolbar_layout.addWidget(self.prev_screen_button)

        self.screen_title_label = ToolbarTitle(screen_title)
        self.toolbar_layout.addWidget(self.screen_title_label)

        self.back_to_home_button = ToolbarButton("Back to Home")
        self.toolbar_layout.addWidget(self.back_to_home_button)

        self.setLayout(self.toolbar_layout)
