from PyQt5.QtWidgets import QComboBox

import style_constants as sc


class Dropdown(QComboBox):
    def __init__(self):
        super().__init__()

        self.dropdown_font = self.font()
        self.dropdown_font.setPointSize(int(sc.FONT_L[0:2]))
        self.setFont(self.dropdown_font)
