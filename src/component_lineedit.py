from PyQt5.QtWidgets import QLineEdit

import style_constants as sc


class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

        self.line_edit_font = self.font()
        self.line_edit_font.setPointSize(int(sc.FONT_XL[0:2]))
        self.setFont(self.line_edit_font)
