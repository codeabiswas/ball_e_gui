from PyQt5.QtWidgets import QPushButton, QSizePolicy


class Button(QPushButton):
    def __init__(self, button_title):
        super().__init__()
        self.setText(button_title)
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        self.setStyleSheet(
            """
            font-size: 30px;
            """
        )
