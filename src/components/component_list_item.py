from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem


class ListItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        font = QFont()
        font.setPixelSize(22)
        self.setFont(font)
