"""
component_lineedit.py
---
This file contains the LineEdit object visually modified as used throughout Ball-E's GUI app
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
    from PyQt5.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    """LineEdit.

    This class configures the QLineEdit object that is used throughtout the GUI for accessibility
    """

    def __init__(self):
        """__init__.

        Configures the QLineEdit object as designed
        """

        super().__init__()

        # Set the font to be big enough for easy view and clickability of the QLineObject itself
        self.line_edit_font = self.font()
        self.line_edit_font.setPointSize(int(sc.FONT_XL[0:2]))
        self.setFont(self.line_edit_font)
