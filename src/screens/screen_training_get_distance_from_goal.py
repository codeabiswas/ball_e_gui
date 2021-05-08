"""
screen_training_get_distance_from_goal.py
---
This file contains the TrainingGetDistanceFromGoalScreen class, which is where the user selects the distance from the goal from a dropdown.
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

    import style_constants as sc
    from component_button import GenericButton
    from component_dropdown import Dropdown
    from component_labels import ProfileLabel
    from component_toolbar import ToolbarComponent
    from helper_profiler import Profiler
    from window_test import TestWindow

except ImportError:
    print("{}: Imports failed".format(__file__))
finally:

    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget


class TrainingGetDistanceFromGoalScreen(QWidget):
    """This class shows a dropdown to the user which allows them to select how far away Ball-E is from the goal (in yards)

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self):
        """Widget Initialization
        """
        super().__init__()

        self.window_title = "Distance from Goal Selection"

        # Create a screen layout object to populate
        self.screen_layout = QVBoxLayout()

        # Create a toolback object and add it to the top of the layout
        self.toolbar = ToolbarComponent(
            self.window_title, "Back to # of Balls\n Select")

        self.screen_layout.addWidget(self.toolbar)

        self.screen_layout.addWidget(ProfileLabel(
            "Please set up Ball-E directly in front of the goal at least {} yards and no further than {} yards away.\nThen, select from the dropdown below how far away (in yards) Ball-E is.".format(sc.MIN_DISTANCE, sc.MAX_DISTANCE)))

        self.curr_dist = sc.MIN_DISTANCE

        distance_input = Dropdown()
        for ball in range(sc.MIN_DISTANCE, sc.MAX_DISTANCE+1):
            distance_input.addItem(str(ball))
        distance_input.currentIndexChanged.connect(
            lambda: self.update_distance(int(distance_input.currentText())))

        self.screen_layout.addWidget(distance_input)

        # Connect this button on the Main Page Window to act accordingly - whether Drill Profile or Manual Session was selected
        self.next_page_button = GenericButton("Next")
        self.next_page_button.setVisible(True)

        self.screen_layout.addWidget(self.next_page_button)

        # Set the screen layout
        self.setLayout(self.screen_layout)

    def update_distance(self, updated_dist):
        """update_distance.

        This function updates the distance selected from the dropdown

        :param updated_dist: String value of the number in the dropdown
        """

        self.curr_dist = updated_dist

    def get_goal_distance(self):
        """get_goal_distance.

        This function returns the current goal distance that the user has selected in feet
        """

        # Return the distance in ft.
        return self.curr_dist*3

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
    win = TestWindow(TrainingGetDistanceFromGoalScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
