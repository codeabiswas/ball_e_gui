"""
screen_training.py
---
This file contains the TrainingSCreen class, which is the Training Screen in Ball-E's GUI.
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

    from component_button import FullPageButton
    from component_toolbar import ToolbarComponent
    from window_test import TestWindow

except ImportError:
    print("{}: Imports failed".format(__file__))
finally:

    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget


class TrainingScreen(QWidget):
    """TrainingScreen.

    This class instantiates and sets up the QWidget object as designed for the Training Screen.
    """

    def __init__(self, parent=None):
        """__init__.

        Initializes the widget accordingly

        :param parent: Default arg.
        """

        super().__init__(parent=parent)

        self.window_title = "Training Screen"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        button_layout = QHBoxLayout()

        self.load_goalie_profile_button = FullPageButton("Load Goalie Profile")
        self.load_drill_profile_button = FullPageButton("Load Drill Profile")
        self.manual_session_button = FullPageButton("Manual Session")

        button_layout.addWidget(self.load_goalie_profile_button)
        button_layout.addWidget(self.load_drill_profile_button)
        button_layout.addWidget(self.manual_session_button)

        screen_layout.addLayout(button_layout)

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
    win = TestWindow(TrainingScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
