"""
screen_help.py
---
This file contains the HelpScreen class, which is the allows the user to navigate different Help sections in Ball-E's GUI
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
        "{}/Developer/ball_e_gui/src/helpers".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/windows".format(pathlib.Path.home()))

    from component_button import FullPageButton
    from component_toolbar import ToolbarComponent
    from window_test import TestWindow
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget


class HelpScreen(QWidget):
    """HelpScreen.

    This class instantiates and sets up the QWidget object with all the appropriate buttons for the Help Screen
    """

    def __init__(self, parent=None):
        """__init__.

        Initializes the widget accordingly

        :param parent: Default arg.
        """
        super().__init__(parent=parent)

        self.window_title = "Help"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        # Create all necessary buttons to navigate to various areas of the help screen
        self.calibration_screen_button = FullPageButton("Calibration")
        self.training_screen_button = FullPageButton("Training")
        self.profiles_screen_button = FullPageButton("Profiles")
        self.session_recording_screen_button = FullPageButton(
            "Session Recording")

        screen_layout.addWidget(self.calibration_screen_button)
        screen_layout.addWidget(self.training_screen_button)
        screen_layout.addWidget(self.profiles_screen_button)
        screen_layout.addWidget(self.session_recording_screen_button)

        self.setLayout(screen_layout)

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
    win = TestWindow(HelpScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
