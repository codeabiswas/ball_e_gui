"""
screen_training_automated_session.py
---
This file contains the TrainingAutomatedSessionScreen class, which is the Automated Training Screen in Ball-E's GUI.
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
    sys.path.append(
        "{}/Developer/ball_e_motor_control/src".format(pathlib.Path.home()))

    from component_button import FullPageButton
    from component_labels import ProfileLabel
    from component_toolbar import ToolbarComponent
    from threaded_drill_session_handler import ThreadedDrillSessionHandler
    from window_test import TestWindow

except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    from PyQt5.QtCore import pyqtSlot
    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget


class TrainingAutomatedSessionScreen(QWidget):
    """Screen for running the automated training session

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self, drill_name, total_ball_num, distance_from_goal,  goalie_name=None):
        """__init__.

        Widget initialization

        :param drill_name: String name of the drill
        :param total_ball_num: Total number of balls in Ball Queue
        :param distance_from_goal: Distance from the goal in feet
        :param goalie_name: String name of the goalie (if this is an automated training session which saves a goalie profile), else None
        """

        super().__init__()

        self.window_title = "Automated Training Session"

        self.drill_name = drill_name
        self.distance_from_goal = distance_from_goal
        self.goalie_name = goalie_name
        self.curr_ball_num = 1
        self.total_ball_num = total_ball_num

        # Object which controls a drill session
        self.drill_handler_thread = ThreadedDrillSessionHandler(
            distance_from_goal=self.distance_from_goal, drill_name=self.drill_name, goalie_name=self.goalie_name)
        self.drill_handler_thread.update_ball_num_signal.connect(
            self.update_ball_num)

        # Create a screen layout object to populate
        self.screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(
            self.window_title, "Back to Goal Calib.")
        self.toolbar.prev_screen_button.setEnabled(False)
        self.toolbar.back_to_home_button.setEnabled(False)

        self.screen_layout.addWidget(self.toolbar)

        self.row_layout = QHBoxLayout()

        self.column_layout = QVBoxLayout()
        self.column_layout.addWidget(ProfileLabel(
            "Running: {}".format(self.drill_name.replace('_', ' ').title())))
        self.ball_number_label = ProfileLabel(
            "Ball {} out of {}".format(self.curr_ball_num, self.total_ball_num))
        self.column_layout.addWidget(self.ball_number_label)

        self.row_layout.addLayout(self.column_layout)

        self.button_layout = QVBoxLayout()

        self.start_button = FullPageButton("Start")
        self.button_layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.on_click_start_button)
        # self.pause_button = FullPageButton("Pause")
        # self.button_layout.addWidget(self.pause_button)
        self.stop_button = FullPageButton("Stop")
        self.button_layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.on_click_stop_button)

        self.row_layout.addLayout(self.button_layout)

        self.screen_layout.addLayout(self.row_layout)

        # Set the screen layout
        self.setLayout(self.screen_layout)

    def on_click_start_button(self):
        """on_click_start_button.
        
        This function starts the drill session when the 'Start' button is clicked
        """

        self.drill_handler_thread.start_drill()
        self.drill_handler_thread.run_automated_drill()

    def on_click_stop_button(self):
        """on_click_stop_button.

        This function stops the drill session when the 'Stop' button is clicked
        """

        self.drill_handler_thread.stop_drill()

    @pyqtSlot(bool)
    def update_ball_num(self, update_bool):
        """update_ball_num.

        When a ball has been shot out and the drill handler notifies us, update the ball number in the UI
        :param update_bool: Boolean value which when True, indicates if a ball has been shot
        """

        if update_bool:
            self.curr_ball_num += 1
            self.ball_number_label.setText(
                "Ball {} out of {}".format(self.curr_ball_num, self.total_ball_num))

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
    win = TestWindow(TrainingAutomatedSessionScreen(
        distance_from_goal=20, drill_name="t_drill", total_ball_num=10))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
