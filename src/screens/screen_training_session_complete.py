"""
screen_training_session_complete.py
---
This file contains the TrainingSessionCompleteScreen class, which is displayed when a Automated or a Manual Training Session is complete/Stopped.
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

    from component_labels import ProfileLabel
    from component_toolbar import ToolbarComponent
    from window_test import TestWindow
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:

    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget


class TrainingSessionCompleteScreen(QWidget):
    """TrainingSessionCompleteScreen.

    This class instantiates the screen which notifies the user that the training session is complete
    """

    def __init__(self, parent=None):
        """__init__.

        Widget initialization

        :param parent: Default arg.
        """

        super().__init__(parent=parent)

        self.window_title = "Training Complete"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        screen_layout.addWidget(ProfileLabel(
            "Training Complete"))

        self.setLayout(screen_layout)

    def get_window_title(self):
        return self.window_title


def main():
    """main.

    Main prototype/testing area. Code prototyping and checking happens here. 
    """

    app = QApplication(sys.argv)
    win = TestWindow(TrainingSessionCompleteScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
