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


class TrainingNumberOfBallsSelectionScreen(QWidget):
    """Screen to create, delete, and view Drill Profiles

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self, prev_screen, drill_name=None):
        """Widget Initialization
        """
        super().__init__()

        self.window_title = "Number of Balls Selection"

        # Create a screen layout object to populate
        self.screen_layout = QVBoxLayout()

        # Create a toolback object and add it to the top of the layout
        if prev_screen == "training_drill_profile_choice_screen":
            self.toolbar = ToolbarComponent(
                self.window_title, "Back to Drill\n Profile Choice")
            # Get the drill profiles available on the device
            self.profiler = Profiler('drill_profiles')
            # Drill TBE: Drill To Be Executed
            self.drill_tbe_path = self.profiler.get_profiles(
            )[drill_name.format(' ', '_').lower()]
            self.required_ball_num = self.get_drill_required_balls()
        elif prev_screen == "training_screen":
            self.toolbar = ToolbarComponent(
                self.window_title, "Back to Training\n Choice")
        else:
            return

        self.screen_layout.addWidget(self.toolbar)

        self.screen_layout.addWidget(ProfileLabel(
            "How many balls are loaded in Ball-E?"))

        self.curr_ball_num = sc.MIN_BALL_COUNT

        number_of_balls_input = Dropdown()
        for ball in range(sc.MIN_BALL_COUNT, sc.MAX_BALL_COUNT+1):
            number_of_balls_input.addItem(str(ball))
        number_of_balls_input.currentIndexChanged.connect(
            lambda: self.update_number_of_balls(int(number_of_balls_input.currentText()), prev_screen))

        self.screen_layout.addWidget(number_of_balls_input)

        if prev_screen == "training_drill_profile_choice_screen":
            self.check_button = GenericButton("Check")
            self.check_button.clicked.connect(self.check_ball_requirement)
            self.screen_layout.addWidget(self.check_button)

        self.enough_balls_label = ProfileLabel("")
        self.enough_balls_label.setVisible(False)
        self.screen_layout.addWidget(self.enough_balls_label)

        # Connect this button on the Main Page Window to act accordingly - whether Drill Profile or Manual Session was selected
        self.next_page_button = GenericButton("Next")
        self.next_page_button.setVisible(False)

        self.screen_layout.addWidget(self.next_page_button)

        # Set the screen layout
        self.setLayout(self.screen_layout)

    def get_drill_required_balls(self):
        drill_plan = self.profiler.get_profile_info(self.drill_tbe_path)
        return len(drill_plan)

    def update_number_of_balls(self, updated_ball_number, prev_screen):
        self.curr_ball_num = updated_ball_number
        if prev_screen == "training_screen":
            self.next_page_button.setVisible(True)

    def get_session_ball_number(self):
        return self.curr_ball_num

    def check_ball_requirement(self):
        if self.curr_ball_num < self.get_drill_required_balls():
            self.enough_balls_label.setText(
                "Selected drill requires {} balls. Please fill at least that many then try again.".format(self.get_drill_required_balls()))
            self.next_page_button.setVisible(False)
        else:
            self.enough_balls_label.setText("You are good to go!")
            self.next_page_button.setVisible(True)

        self.enough_balls_label.setVisible(True)

    def reset_screen(self):

        self.enough_balls_label.setVisible(False)

    def get_window_title(self):
        """Helper function to return this window's title

        Returns:
            [string]: This window's title
        """
        return self.window_title


def main():
    app = QApplication(sys.argv)
    # win = TestWindow(TrainingNumberOfBallsSelectionScreen(
    #     prev_screen="training_screen"))
    win = TestWindow(TrainingNumberOfBallsSelectionScreen(
        prev_screen="training_drill_profile_choice_screen", drill_name="drill_a"))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
