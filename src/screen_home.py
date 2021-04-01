import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from window_test import TestWindow


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
            font-size: 80px;
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


class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Home"

        home_screen_layout = QVBoxLayout()

        top_portion_layout = QHBoxLayout()

        title_subtitle_layout = QVBoxLayout()

        title_subtitle_layout.addWidget(HomeScreenTitle("Ball-E"))
        title_subtitle_layout.addWidget(
            HomeScreenSubtitle("The Robotic Lacrosse Goalie Trainer"))
        top_portion_layout.addLayout(title_subtitle_layout)

        power_off_button = PowerOffButton("Power-Off")
        power_off_button.clicked.connect(self.OnClickPowerOffButton)

        top_portion_layout.addWidget(power_off_button)

        home_screen_layout.addLayout(top_portion_layout)

        self.training_button = HomeScreenButton("Training")
        self.profiles_button = HomeScreenButton("Profiles")
        self.help_button = HomeScreenButton("Help")

        home_screen_layout.addWidget(self.training_button)
        home_screen_layout.addWidget(self.profiles_button)
        home_screen_layout.addWidget(self.help_button)

        self.setLayout(home_screen_layout)

    def OnClickPowerOffButton(self):
        sys.exit()

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(HomeScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
