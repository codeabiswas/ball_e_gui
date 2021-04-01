from PyQt5.QtWidgets import QLabel

import style_constants as sc


class ProfileLabel(QLabel):
    def __init__(self, profile_label):
        super().__init__()
        self.setText(profile_label)
        self.setStyleSheet(
            """
            color: black;
            font-size: {font_size};
            """.format(font_size=sc.FONT_L)
        )


class TableHeaderLabel(QLabel):
    def __init__(self, table_header_label):
        super().__init__()
        self.setText(table_header_label)
        self.setStyleSheet(
            """
            color: black;
            font-size: {font_size};
            font-weight: bold;
            """.format(font_size=sc.FONT_L)
        )
