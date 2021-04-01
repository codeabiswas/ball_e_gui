from PyQt5.QtWidgets import QPushButton, QSizePolicy

import style_constants as sc


class GenericButton(QPushButton):
    def __init__(self, button_title):
        super().__init__()
        self.setText(button_title)
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        self.setMaximumHeight(int(sc.FONT_XL[:2]))

        self.setStyleSheet(
            """
            font-size: {font_size};
            """.format(font_size=sc.FONT_L)
        )


class FullPageButton(QPushButton):
    def __init__(self, button_title):
        super().__init__()
        self.setText(button_title)
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        self.setStyleSheet(
            """
            font-size: {font_size};
            """.format(font_size=sc.FONT_L)
        )


class ProfileCreateButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Create New")
        self.setFixedWidth(150)
        self.setStyleSheet(
            """
            background-color: green;
            color: white;
            font-size: {font_size};
            font-weight: bold;
            """.format(font_size=sc.FONT_M)
        )


class ProfileDeleteButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Delete")
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )
        self.setFixedWidth(100)
        self.setStyleSheet(
            """
            background-color: red;
            color: white;
            font-size: {font_size};
            font-weight: bold;
            """.format(font_size=sc.FONT_S)
        )
