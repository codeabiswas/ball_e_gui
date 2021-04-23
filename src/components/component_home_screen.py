from PyQt5.QtWidgets import QLabel, QPushButton, QSizePolicy


class HomeScreenButton(QPushButton):
    def __init__(self, button_text):
        super().__init__()
        self.button_text = button_text
        self.setText(self.button_text)
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )
        self.setStyleSheet(
            """
            background-color: green;
            color: white;
            font-size: 60px;
            font-weight: bold;
            """
        )


class PowerOffButton(QPushButton):
    def __init__(self, button_text):
        super().__init__()
        self.button_text = button_text
        self.setText(self.button_text)
        self.setFixedHeight(400)
        self.setFixedWidth(400)
        self.setStyleSheet(
            """
            background-color: red;
            color: white;
            font-size: 40px;
            font-weight: bold;
            """
        )


class HomeScreenTitle(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(
            """
            color: black;
            font-size: 100px;
            font-weight: bold
            """
        )


class HomeScreenSubtitle(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(
            """
            color: black;
            font-size: 60px;
            """
        )
