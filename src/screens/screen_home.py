try:
    import pathlib
    import sys
    sys.path.append(
        "{}/Developer/ball_e_gui/src/components".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/windows".format(pathlib.Path.home()))

    from component_home_screen import (HomeScreenButton, HomeScreenSubtitle,
                                       HomeScreenTitle, PowerOffButton)
    from window_test import TestWindow
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    import os

    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget


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
        os.system("shutdown /s /t 0")
        # sys.exit()

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(HomeScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
