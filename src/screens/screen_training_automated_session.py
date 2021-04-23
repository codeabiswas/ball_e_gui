try:
    import pathlib
    import sys
    sys.path.append(
        "{}/Developer/ball_e_gui/src/components".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/windows".format(pathlib.Path.home()))

    from component_button import FullPageButton
    from component_labels import ProfileLabel
    from component_toolbar import ToolbarComponent
    from window_test import TestWindow

except ImportError:
    print("Imports failed")
finally:

    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget


class TrainingAutomatedSessionScreen(QWidget):
    """Screen to create, delete, and view Drill Profiles

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self, drill_name, total_ball_num):
        """Widget Initialization
        """
        super().__init__()

        self.window_title = "Automated Training Session"

        self.drill_name = drill_name
        self.curr_ball_num = 1
        self.total_ball_num = total_ball_num

        # Create a screen layout object to populate
        self.screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(
            self.window_title, "Back to Goal Calib.")

        self.screen_layout.addWidget(self.toolbar)

        self.row_layout = QHBoxLayout()

        self.column_layout = QVBoxLayout()
        self.column_layout.addWidget(ProfileLabel(
            "Running: {}".format(self.drill_name)))
        self.ball_number_label = ProfileLabel(
            "Ball {} out of {}".format(self.curr_ball_num, self.total_ball_num))
        self.column_layout.addWidget(self.ball_number_label)

        self.row_layout.addLayout(self.column_layout)

        self.button_layout = QVBoxLayout()

        self.start_button = FullPageButton("Start")
        self.button_layout.addWidget(self.start_button)
        self.pause_button = FullPageButton("Pause")
        self.button_layout.addWidget(self.pause_button)
        self.stop_button = FullPageButton("Stop")
        self.button_layout.addWidget(self.stop_button)

        self.row_layout.addLayout(self.button_layout)

        self.screen_layout.addLayout(self.row_layout)

        # Set the screen layout
        self.setLayout(self.screen_layout)

    def get_window_title(self):
        """Helper function to return this window's title

        Returns:
            [string]: This window's title
        """
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingAutomatedSessionScreen("Drill A", 20))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
