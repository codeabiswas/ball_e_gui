import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

import screen_drill_profiles
import screen_goalie_profiles
import screen_help
import screen_help_calibration
import screen_help_profiles
import screen_help_session_recording
import screen_help_training
import screen_home
import screen_profiles
import screen_training
import screen_training_automated_session
import screen_training_drill_profile_selection
import screen_training_goal_calibration
import screen_training_goal_calibration_take_photo
import screen_training_goalie_profile_selection
import screen_training_manual_session
import screen_training_number_of_balls_selection
import screen_training_session_recording_check


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Whether or not a Manual Session has been selected by user, defaults to False
        self.manual_session = False

        # All screens setup
        self.home_screen = screen_home.HomeScreen()

        self.training_screen = screen_training.TrainingScreen()
        self.training_goalie_profile_selection_screen = screen_training_goalie_profile_selection.TrainingGoalieProfileSelectionScreen()
        self.training_drill_profile_selection_screen = screen_training_drill_profile_selection.TrainingDrillProfileSelectionScreen()
        # For the Number of Balls selection screen, the previous screen needs to be known, therefore it will be called from the respective flow
        self.training_session_recording_check_screen = screen_training_session_recording_check.TrainingSessionRecordingCheckScreen()
        self.training_goal_calibration_take_photo_screen = screen_training_goal_calibration_take_photo.TrainingGoalCalibrationTakePhotoScreen()
        self.training_goal_calibration_screen = screen_training_goal_calibration.TrainingGoalCalibration()

        self.profiles_screen = screen_profiles.ProfilesScreen()
        self.goalie_profiles_screen = screen_goalie_profiles.GoalieProfilesScreen()
        self.drill_profiles_screen = screen_drill_profiles.DrillProfilesScreen()

        self.help_screen = screen_help.HelpScreen()
        self.calibration_help_screen = screen_help_calibration.CalibrationHelpScreen()
        self.training_help_screen = screen_help_training.TrainingHelpScreen()
        self.profiles_help_screen = screen_help_profiles.ProfilesHelpScreen()
        self.session_recording_help_screen = screen_help_session_recording.SessionRecordingHelpScreen()

        # The Stacked Widget
        self.main_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.main_widget)

        # Adding all screens to the stacked widget
        self.main_widget.addWidget(self.home_screen)

        self.main_widget.addWidget(self.training_screen)
        self.main_widget.addWidget(
            self.training_goalie_profile_selection_screen)
        self.main_widget.addWidget(
            self.training_drill_profile_selection_screen)
        self.main_widget.addWidget(
            self.training_session_recording_check_screen)
        self.main_widget.addWidget(
            self.training_goal_calibration_take_photo_screen)
        self.main_widget.addWidget(
            self.training_goal_calibration_screen)

        self.main_widget.addWidget(self.profiles_screen)
        self.main_widget.addWidget(self.goalie_profiles_screen)
        self.main_widget.addWidget(self.drill_profiles_screen)

        self.main_widget.addWidget(self.help_screen)
        self.main_widget.addWidget(self.calibration_help_screen)
        self.main_widget.addWidget(self.training_help_screen)
        self.main_widget.addWidget(self.profiles_help_screen)
        self.main_widget.addWidget(self.session_recording_help_screen)

        # For program startup, set it as the current widget
        self.main_widget.setCurrentWidget(self.home_screen)

        # Home Screen Flows
        self.home_screen_flows()

        # Training Screen Flows
        self.training_screen_flows()
        self.training_goalie_profile_selection_screen_flows()
        self.training_drill_profile_selection_screen_flows()
        self.training_session_recording_check_screen_flows()
        self.training_goal_calibration_take_photo_screen_flows()
        self.training_goal_calibration_screen_flows()

        # Profiles Screen Flows
        self.profiles_screen_flows()
        # Goalie Profiles Screen Flows
        self.goalie_profiles_screen_flows()
        # Drill Profiles Screen Flows
        self.drill_profiles_screen_flows()

        # Help Screen Flows
        self.help_screen_flows()
        # Calibration Help Screen Flows
        self.calibration_help_screen_flows()
        # Training Help Screen Flows
        self.training_help_screen_flows()
        # Profiles Help Screen Flows
        self.profiles_help_screen_flows()
        # Session Recording Help Screen Flows
        self.session_recording_help_screen_flows()

    def home_screen_flows(self):
        # Home Screen Flows
        self.home_screen.training_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_screen))
        self.home_screen.profiles_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.profiles_screen))
        self.home_screen.help_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def training_screen_flows(self):
        # Toolbar Flows
        self.training_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))

        # Training Screen Flows
        self.training_screen.load_goalie_profile_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(
                self.training_goalie_profile_selection_screen)
        )
        self.training_screen.load_drill_profile_button.clicked.connect(
            self.only_training_drill_profile_profile_selection_screen_setup
        )
        self.training_screen.manual_session_button.clicked.connect(
            self.manual_session_training_number_of_balls_selection_screen_setup
        )

    def manual_session_training_number_of_balls_selection_screen_setup(self):
        self.manual_session = True
        prev_screen = "training_screen"

        self.training_number_of_balls_selection_screen = screen_training_number_of_balls_selection.TrainingNumberOfBallsSelectionScreen(
            prev_screen=prev_screen)

        self.training_number_of_balls_selection_screen_flows(
            prev_screen=prev_screen)

        self.main_widget.addWidget(
            self.training_number_of_balls_selection_screen)
        self.main_widget.setCurrentWidget(
            self.training_number_of_balls_selection_screen)

    def training_number_of_balls_selection_screen_flows(self, prev_screen):
        # Toolbar Flows
        self.training_number_of_balls_selection_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        if prev_screen == "training_screen":
            self.training_number_of_balls_selection_screen.toolbar.prev_screen_button.clicked.connect(
                lambda: self.main_widget.setCurrentWidget(self.training_screen))
        elif prev_screen == "training_drill_profile_choice_screen":
            self.training_number_of_balls_selection_screen.toolbar.prev_screen_button.clicked.connect(
                lambda: self.main_widget.setCurrentWidget(self.training_drill_profile_selection_screen))
        else:
            return

        self.training_number_of_balls_selection_screen.next_page_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(
                self.training_session_recording_check_screen)
        )

    def only_training_drill_profile_profile_selection_screen_setup(self):
        self.manual_session = False

        self.training_drill_profile_selection_screen = screen_training_drill_profile_selection.TrainingDrillProfileSelectionScreen()

        self.main_widget.addWidget(
            self.training_drill_profile_selection_screen)

        self.training_drill_profile_selection_screen_flows(
            goalie_selected=None)

        self.main_widget.setCurrentWidget(
            self.training_drill_profile_selection_screen)

    def training_goalie_profile_selection_screen_flows(self):
        # Toolbar Flows
        self.training_goalie_profile_selection_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_goalie_profile_selection_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_screen))

        # Training Goalie Profile Selection Screen Flows
        # Repopulate the Drill Selection page according to the Goalie Profile Selection flow
        self.training_goalie_profile_selection_screen.next_page_button.clicked.connect(
            self.training_goalie_then_drill_profile_selection_screen_setup
        )

    def training_goalie_then_drill_profile_selection_screen_setup(self):
        self.manual_session = False

        goalie_selected = self.training_goalie_profile_selection_screen.get_selected_goalie_profile()

        self.training_goalie_profile_selection_screen.reset_screen()

        self.training_drill_profile_selection_screen = screen_training_drill_profile_selection.TrainingDrillProfileSelectionScreen(
            goalie_selected)

        self.main_widget.addWidget(
            self.training_drill_profile_selection_screen)

        self.training_drill_profile_selection_screen_flows(
            goalie_selected=goalie_selected)

        self.main_widget.setCurrentWidget(
            self.training_drill_profile_selection_screen)

    def training_drill_profile_selection_screen_flows(self, goalie_selected=None):
        # Toolbar Flows
        self.training_drill_profile_selection_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        if goalie_selected is None:
            self.training_drill_profile_selection_screen.toolbar.prev_screen_button.clicked.connect(
                lambda: self.main_widget.setCurrentWidget(self.training_screen))
        else:
            self.training_drill_profile_selection_screen.toolbar.prev_screen_button.clicked.connect(
                lambda: self.main_widget.setCurrentWidget(self.training_goalie_profile_selection_screen))

        self.training_drill_profile_selection_screen.next_page_button.clicked.connect(
            lambda: self.automated_session_training_number_of_balls_selection_screen_setup(self.training_drill_profile_selection_screen.get_selected_drill_profile()))

    def automated_session_training_number_of_balls_selection_screen_setup(self,  drill_name):
        prev_screen = "training_drill_profile_choice_screen"

        self.training_number_of_balls_selection_screen = screen_training_number_of_balls_selection.TrainingNumberOfBallsSelectionScreen(
            prev_screen=prev_screen, drill_name=drill_name)

        self.training_number_of_balls_selection_screen_flows(
            prev_screen=prev_screen)

        self.main_widget.addWidget(
            self.training_number_of_balls_selection_screen)
        self.main_widget.setCurrentWidget(
            self.training_number_of_balls_selection_screen)

    def training_session_recording_check_screen_flows(self):
        # Toolbar Flows
        self.training_session_recording_check_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_session_recording_check_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_number_of_balls_selection_screen))

        # Screen Flows
        self.training_session_recording_check_screen.next_page_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_goal_calibration_take_photo_screen))

    def training_goal_calibration_take_photo_screen_flows(self):
        # Toolbar Flows
        self.training_goal_calibration_take_photo_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_goal_calibration_take_photo_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_session_recording_check_screen))

        # Screen Flows
        self.training_goal_calibration_take_photo_screen.next_page_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_goal_calibration_screen))

    def training_goal_calibration_screen_flows(self):
        # Toolbar Flows
        self.training_goal_calibration_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_goal_calibration_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_goal_calibration_take_photo_screen))

        # Screen Flows
        self.training_goal_calibration_screen.next_page_button.clicked.connect(
            self.training_auomated_or_manual_session_screen_setup)

    def training_automated_or_manual_session_screen_setup(self):
        if self.manual_session:
            self.training_manual_session_screen = screen_training_manual_session.TrainingManualSessionScreen(
                self.training_number_of_balls_selection_screen.get_session_ball_number()
            )
            self.training_manual_session_screen_flows()
            self.main_widget.addWidget(self.training_manual_session_screen)
            self.main_widget.setCurrentWidget(
                self.training_manual_session_screen)
        else:
            self.training_automated_session_screen = screen_training_automated_session.TrainingAutomatedSessionScreen(
                self.training_drill_profile_selection_screen.get_selected_drill_profile(), self.training_number_of_balls_selection_screen.get_session_ball_number())
            self.training_automated_session_screen_flows()
            self.main_widget.addWidget(self.training_automated_session_screen)
            self.main_widget.setCurrentWidget(
                self.training_automated_session_screen)

    def training_automated_session_screen_flows(self):
        # Toolbar Flows
        self.training_automated_session_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_automated_session_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_goal_calibration_screen))

    def training_manual_session_screen_flows(self):
        # Toolbar Flows
        self.training_manual_session_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_manual_session_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_goal_calibration_screen))

    def profiles_screen_flows(self):
        # Toolbar Flows
        self.profiles_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))

        # Profiles Screen Flows
        self.profiles_screen.goalie_profiles_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.goalie_profiles_screen))
        self.profiles_screen.drill_profiles_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.drill_profiles_screen))

    def goalie_profiles_screen_flows(self):
        # Toolbar Flows
        self.goalie_profiles_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.goalie_profiles_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.profiles_screen))

    def drill_profiles_screen_flows(self):
        # Toolbar Flows
        self.drill_profiles_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.drill_profiles_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.profiles_screen))

    def help_screen_flows(self):

        # Toolbar Flows
        self.help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))

        # Help Screen Flows
        self.help_screen.calibration_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.calibration_help_screen))
        self.help_screen.training_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_help_screen))
        self.help_screen.profiles_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.profiles_help_screen))
        self.help_screen.session_recording_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.session_recording_help_screen))

    def calibration_help_screen_flows(self):

        # Toolbar Flows
        self.calibration_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.calibration_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def training_help_screen_flows(self):

        # Toolbar Flows
        self.training_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def profiles_help_screen_flows(self):

        # Toolbar Flows
        self.profiles_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.profiles_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def session_recording_help_screen_flows(self):

        # Toolbar Flows
        self.session_recording_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.session_recording_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
