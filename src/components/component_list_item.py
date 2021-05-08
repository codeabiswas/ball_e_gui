"""
component_list_item.py
---
This file contains the ListItem object that is used through Ball-E's GUI for the List object
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem


class ListItem(QListWidgetItem):
    """ListItem.

    This class configures the QListWidgetItem visually that is used throughtout the GUI for easy visibility.
    """

    def __init__(self, text):
        """__init__.

        Configures the QListWidgetItem object as designed

        :param text: String which contains the text that is displayed in this object
        """

        super().__init__()
        # Set the text of the object
        self.setText(text)
        # Set the font size of the object
        font = QFont()
        font.setPixelSize(22)
        self.setFont(font)
