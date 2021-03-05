import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)


class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        home_screen_layout = QVBoxLayout()

        power_off_button = QPushButton("Power-Off")
        power_off_button.clicked.connect(self.OnClickPowerOffButton)
        home_screen_layout.addWidget(power_off_button)

        home_screen_layout.addWidget(QLabel("Ball-E"))
        home_screen_layout.addWidget(QLabel("Robotic Lacrosse Goalie Trainer"))

        self.training_button = QPushButton("Training")
        # training_button.clicked.connect(self.OnClickTrainingButton)
        self.profiles_button = QPushButton("Profiles")
        # profiles_button.clicked.connect(self.OnClickProfilesButton)
        self.help_button = QPushButton("Help")
        # help_button.clicked.connect(self.OnClickHelpButton)

        home_screen_layout.addWidget(self.training_button)
        home_screen_layout.addWidget(self.profiles_button)
        home_screen_layout.addWidget(self.help_button)

        self.setLayout(home_screen_layout)

    def OnClickPowerOffButton(self):
        sys.exit()

    def OnClickTrainingButton(self):
        print("Training Button Pressed")

    def OnClickProfilesButton(self):
        print("Profiles Button Pressed")

    def OnClickHelpButton(self):
        print("Help Button Pressed")


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setWindowTitle('Home Screen')
        self.setCentralWidget(HomeScreen())


def main():
    app = QApplication(sys.argv)
    win = TestWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
