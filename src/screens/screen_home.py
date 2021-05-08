"""
screen_home.py
---
This file contains the HomeScreen class, which is the Home Screen in Ball-E's GUI.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

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
    """HomeScreen.

    This class instantiates and sets up the QWidget object as designed for the Home Screen.
    """

    def __init__(self, parent=None):
        """__init__.

        Initializes the widget accordingly

        :param parent: Default arg.
        """

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
        """OnClickPowerOffButton.

        This functions turns off the Jetson Nano after the user clicks on the Power-Off Button
        """

        os.system("systemctl poweroff")

    def get_window_title(self):
        """Helper function to return this window's title

        Returns:
            [string]: This window's title
        """

        return self.window_title


def main():
    """main.

    Main prototype/testing area. Code prototyping and checking happens here. 
    """

    app = QApplication(sys.argv)
    win = TestWindow(HomeScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
