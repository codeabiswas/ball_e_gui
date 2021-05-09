"""
component_dropdown.py
---
This file contains the class required to configure the Dropdown object used throughout Ball-E's GUI app.
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
    from PyQt5.QtWidgets import QComboBox


class Dropdown(QComboBox):
    """Dropdown.

    This class configures a generic QComboBox (i.e.: Dropdown) which is used throughout the GUI
    """

    def __init__(self):
        """__init__.

        Configures the QComboBox object as designed
        """
        super().__init__()

        self.dropdown_font = self.font()
        self.dropdown_font.setPointSize(int(sc.FONT_XL[0:2]))
        self.setFont(self.dropdown_font)
