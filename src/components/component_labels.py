"""
component_labels.py
---
This file contains the various classes required to configure various types of labels for the GUI app for Ball-E.
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
    from PyQt5.QtWidgets import QLabel


class ProfileLabel(QLabel):
    """ProfileLabel.

    This class configures and customizes the QLabel object used throughout most of the GUI for its big font.
    """

    def __init__(self, profile_label):
        """__init__.

        Configures the QLabel object as designed.

        :param profile_label: String which contains the text that must be displayed in this object
        """

        super().__init__()
        # Set the text of the QLabel
        self.setText(profile_label)
        # Use CSS to configure the text color and the font-size of this label
        self.setStyleSheet(
            """
            color: black;
            font-size: {font_size};
            """.format(font_size=sc.FONT_L)
        )


class TableHeaderLabel(QLabel):
    """TableHeaderLabel.

    This class configures and customizes the QLabel object used in Table Headers.
    """

    def __init__(self, table_header_label):
        """__init__.

        Configures the QLabel object as designed.

        :param table_header_label: String which contains the text that must be displayed in this object
        """

        super().__init__()
        # Set the text of the QLabel
        self.setText(table_header_label)
        # Use CSS to configure the text color, font-size, and font-weight of this label
        self.setStyleSheet(
            """
            color: black;
            font-size: {font_size};
            font-weight: bold;
            """.format(font_size=sc.FONT_L)
        )
