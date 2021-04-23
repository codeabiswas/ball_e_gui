from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow


class TestWindow(QMainWindow):
    def __init__(self, some_widget, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setWindowTitle(some_widget.get_window_title())
        self.setCentralWidget(some_widget)
