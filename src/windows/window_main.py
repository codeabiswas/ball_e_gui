"""
window_main.py
---
This file contains the MainWindow class. It is the frameless window which controls and displays all the screens (i.e.: QWidget Objects) in Ball-E's user interface.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

try:
    import sys
    from pathlib import Path
    sys.path.append(
        "{}/Developer/ball_e_gui/src/screens".format(Path.home()))
    import screen_drill_profiles
    import screen_goalie_profiles
    import screen_help
    import screen_help_calibration
    import screen_help_profiles
    import screen_help_training
    import screen_help_using_ball_e
    import screen_home
    import screen_profiles
    import screen_training
    import screen_training_automated_session
    import screen_training_drill_profile_selection
    import screen_training_get_distance_from_goal
    # import screen_training_goal_calibration
    # import screen_training_goal_calibration_take_photo
    import screen_training_goalie_profile_selection
    import screen_training_manual_session
    import screen_training_number_of_balls_selection
    import screen_training_session_complete

    # import screen_training_session_recording_check
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt, pyqtSlot
    from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    """MainWindow.

    This class creates a frameless window around a Stacked Widget object, which contains all the QWidget objects in the UI.
    """

    def __init__(self, parent=None):
        """__init__.

        Initalizes the QMainWindow object with appropriate arguments

        :param parent: Default arg.
        """
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Whether or not a Manual Session has been selected by user, defaults to False
        self.manual_session = False
        # Whether or not an Automated Session using a Goalie Profile has been selected by user, defaults to False
        self.automated_with_goalie_session = False

        # All screens setup
        self.home_screen = screen_home.HomeScreen()

        # Instantiate Training screens objects
        self.training_screen = screen_training.TrainingScreen()
        self.training_goalie_profile_selection_screen = screen_training_goalie_profile_selection.TrainingGoalieProfileSelectionScreen()
        self.training_drill_profile_selection_screen = screen_training_drill_profile_selection.TrainingDrillProfileSelectionScreen()
        # For the Number of Balls selection screen, the previous screen needs to be known, therefore it will be called from the respective flow
        # self.training_session_recording_check_screen = screen_training_session_recording_check.TrainingSessionRecordingCheckScreen()
        # self.training_goal_calibration_take_photo_screen = screen_training_goal_calibration_take_photo.TrainingGoalCalibrationTakePhotoScreen()
        # self.training_goal_calibration_screen = screen_training_goal_calibration.TrainingGoalCalibrationScreen()
        self.training_get_distance_from_goal_screen = screen_training_get_distance_from_goal.TrainingGetDistanceFromGoalScreen()
        self.training_session_complete_screen = screen_training_session_complete.TrainingSessionCompleteScreen()

        # Instantiate Profiles screens objects
        self.profiles_screen = screen_profiles.ProfilesScreen()
        self.goalie_profiles_screen = screen_goalie_profiles.GoalieProfilesScreen()
        self.drill_profiles_screen = screen_drill_profiles.DrillProfilesScreen()

        # Instantiate Help screens objects
        self.help_screen = screen_help.HelpScreen()
        self.calibration_help_screen = screen_help_calibration.CalibrationHelpScreen()
        self.training_help_screen = screen_help_training.TrainingHelpScreen()
        self.profiles_help_screen = screen_help_profiles.ProfilesHelpScreen()
        self.using_ball_e_help_screen = screen_help_using_ball_e.UsingBallEHelpScreen()

        # The Stacked Widget
        self.main_widget = QtWidgets.QStackedWidget()
        # When the widget in the stacked widget changes, it will call this function
        self.main_widget.currentChanged.connect(self.stacked_widget_updated)
        self.setCentralWidget(self.main_widget)

        # Adding all screens to the stacked widget
        self.main_widget.addWidget(self.home_screen)

        # Add all instantiated Training screen objects above
        self.main_widget.addWidget(self.training_screen)
        self.main_widget.addWidget(
            self.training_goalie_profile_selection_screen)
        self.main_widget.addWidget(
            self.training_drill_profile_selection_screen)
        self.main_widget.addWidget(
            self.training_get_distance_from_goal_screen
        )
        # self.main_widget.addWidget(
        #     self.training_session_recording_check_screen)
        # self.main_widget.addWidget(
        #     self.training_goal_calibration_take_photo_screen)
        # self.main_widget.addWidget(
        #     self.training_goal_calibration_screen)
        self.main_widget.addWidget(
            self.training_session_complete_screen)

        # Add all instantiated Profiles screen objects above
        self.main_widget.addWidget(self.profiles_screen)
        self.main_widget.addWidget(self.goalie_profiles_screen)
        self.main_widget.addWidget(self.drill_profiles_screen)

        # Add all instantiated Help screen objects above
        self.main_widget.addWidget(self.help_screen)
        self.main_widget.addWidget(self.calibration_help_screen)
        self.main_widget.addWidget(self.training_help_screen)
        self.main_widget.addWidget(self.profiles_help_screen)
        self.main_widget.addWidget(self.using_ball_e_help_screen)

        # For program startup, set it as the current widget
        self.main_widget.setCurrentWidget(self.home_screen)

        # Home Screen Flows
        self.home_screen_flows()

        # Training Screen Flows
        self.training_screen_flows()
        self.training_goalie_profile_selection_screen_flows()
        self.training_drill_profile_selection_screen_flows()
        # self.training_session_recording_check_screen_flows()
        # self.training_goal_calibration_take_photo_screen_flows()
        # self.training_goal_calibration_screen_flows()
        self.training_get_distance_from_goal_screen_flows()
        self.training_session_complete_screen_flows()

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
        self.using_ball_e_help_screen_flows()

    def stacked_widget_updated(self, index):
        """stacked_widget_updated.

        This function gets called whenever the stacked widget displays a new QWidget object

        :param index: Integer index of what the current stacked widget is at
        """
        curr_widget = self.main_widget.currentWidget()
        # Extract the class name
        curr_widget_class_name = curr_widget.__class__.__name__

        # Handles special cases given which widget is currently displayed
        if curr_widget_class_name == "TrainingGoalieProfileSelectionScreen":
            self.automated_with_goalie_session = True
            self.training_goalie_profile_selection_screen.update_profiles()
        elif curr_widget_class_name == "TrainingDrillProfileSelectionScreen":
            self.training_drill_profile_selection_screen.update_profiles()
        elif curr_widget_class_name == "TrainingGoalCalibrationScreen":
            self.training_goal_calibration_screen.update_lax_goal_pic()
        elif curr_widget_class_name == "TrainingScreen":
            self.manual_session = False
            self.automated_with_goalie_session = False

    def home_screen_flows(self):
        """home_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Home Screen Flows
        self.home_screen.training_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_screen))
        self.home_screen.profiles_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.profiles_screen))
        self.home_screen.help_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def training_screen_flows(self):
        """training_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))

        # Training Screen Flows
        self.training_screen.load_goalie_profile_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(
                self.training_goalie_profile_selection_screen)
        )
        self.training_screen.load_drill_profile_button.clicked.connect(
            self.helper_only_training_drill_profile_profile_selection_screen_setup
        )
        self.training_screen.manual_session_button.clicked.connect(
            self.helper_manual_session_training_number_of_balls_selection_screen_setup
        )

    def helper_manual_session_training_number_of_balls_selection_screen_setup(self):
        """helper_manual_session_training_number_of_balls_selection_screen_setup.

        This function executes all necessary setup that needs to happen before actually going into the screens appropriate flows, such as getting some information from the previous page, etc.
        """
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
        """training_number_of_balls_selection_screen_flows.

        This function executes all necessary setup that needs to happen before actually going into the screens appropriate flows, such as getting some information from the previous page, etc.

        :param prev_screen: String name of the previous screen
        """
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
                self.training_get_distance_from_goal_screen)
        )

    def helper_only_training_drill_profile_profile_selection_screen_setup(self):
        """helper_only_training_drill_profile_profile_selection_screen_setup.

        This function executes all necessary setup that needs to happen before actually going into the screens appropriate flows, such as getting some information from the previous page, etc.
        """
        self.manual_session = False

        self.training_drill_profile_selection_screen = screen_training_drill_profile_selection.TrainingDrillProfileSelectionScreen()

        self.main_widget.addWidget(
            self.training_drill_profile_selection_screen)

        self.training_drill_profile_selection_screen_flows(
            goalie_selected=None)

        self.main_widget.setCurrentWidget(
            self.training_drill_profile_selection_screen)

    def training_goalie_profile_selection_screen_flows(self):
        """training_goalie_profile_selection_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
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
        """training_goalie_then_drill_profile_selection_screen_setup.

        This function executes all necessary setup that needs to happen before actually going into the screens appropriate flows, such as getting some information from the previous page, etc.
        """
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
        """training_drill_profile_selection_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.

        :param goalie_selected: String name of the goalie profile selected
        """
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
            lambda: self.helper_automated_session_training_number_of_balls_selection_screen_setup(self.training_drill_profile_selection_screen.get_selected_drill_profile()))

    def helper_automated_session_training_number_of_balls_selection_screen_setup(self,  drill_name):
        """helper_automated_session_training_number_of_balls_selection_screen_setup.

        This function executes all necessary setup that needs to happen before actually going into the screens appropriate flows, such as getting some information from the previous page, etc.

        :param drill_name: String name of the drill profile selected
        """
        prev_screen = "training_drill_profile_choice_screen"

        self.training_number_of_balls_selection_screen = screen_training_number_of_balls_selection.TrainingNumberOfBallsSelectionScreen(
            prev_screen=prev_screen, drill_name=drill_name)

        self.training_number_of_balls_selection_screen_flows(
            prev_screen=prev_screen)

        self.main_widget.addWidget(
            self.training_number_of_balls_selection_screen)
        self.main_widget.setCurrentWidget(
            self.training_number_of_balls_selection_screen)

    def training_get_distance_from_goal_screen_flows(self):
        """training_get_distance_from_goal_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_get_distance_from_goal_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_get_distance_from_goal_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_number_of_balls_selection_screen))

        # Screen Flows
        self.training_get_distance_from_goal_screen.next_page_button.clicked.connect(
            self.training_automated_or_manual_session_screen_setup)

    def training_session_recording_check_screen_flows(self):
        """training_session_recording_check_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_session_recording_check_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_session_recording_check_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_number_of_balls_selection_screen))

        # Screen Flows
        self.training_session_recording_check_screen.next_page_button.clicked.connect(
            self.training_goal_calibration_take_photo_screen_startup_steps)

    def training_goal_calibration_take_photo_screen_flows(self):
        """training_goal_calibration_take_photo_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_goal_calibration_take_photo_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.training_goal_calibration_take_photo_screen_closing_steps("home_screen"))
        self.training_goal_calibration_take_photo_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.training_goal_calibration_take_photo_screen_closing_steps("prev_screen"))

        # Screen Flows
        self.training_goal_calibration_take_photo_screen.next_page_button.clicked.connect(
            lambda: self.training_goal_calibration_take_photo_screen_closing_steps("next_screen"))

    def training_goal_calibration_take_photo_screen_startup_steps(self):
        """training_goal_calibration_take_photo_screen_startup_steps.

        This function's purpose is to ensure that the camera object has been started properly.
        """

        self.main_widget.setCurrentWidget(
            self.training_goal_calibration_take_photo_screen)

        self.training_goal_calibration_take_photo_screen.start_camera()

    def training_goal_calibration_take_photo_screen_closing_steps(self, button_type):
        """training_goal_calibration_take_photo_screen_closing_steps.

        This function's purpose is to ensure that the camera object has been stopped, closed, and cleared properly. Then navigating the user to the right screen.

        :param button_type: String name of which button was clicked
        """

        self.training_goal_calibration_take_photo_screen.cleanup_steps()

        if button_type == "home_screen":
            self.main_widget.setCurrentWidget(
                self.home_screen)
        elif button_type == "prev_screen":
            self.main_widget.setCurrentWidget(
                self.training_session_recording_check_screen)
        elif button_type == "next_screen":
            self.main_widget.setCurrentWidget(
                self.training_goal_calibration_screen)

    def training_goal_calibration_screen_flows(self):
        """training_goal_calibration_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_goal_calibration_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_goal_calibration_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_goal_calibration_take_photo_screen))

        # Screen Flows
        self.training_goal_calibration_screen.next_page_button.clicked.connect(
            self.training_automated_or_manual_session_screen_setup)

    def training_automated_or_manual_session_screen_setup(self):
        """training_automated_or_manual_session_screen_setup.

        This function executes all necessary setup that needs to happen before actually going into the screens appropriate flows, such as getting some information from the previous page, etc.
        """
        # If a manual session has been selected
        if self.manual_session:
            # Instantiate a manual screen QWidget
            self.training_manual_session_screen = screen_training_manual_session.TrainingManualSessionScreen(
                total_ball_num=self.training_number_of_balls_selection_screen.get_session_ball_number(
                ), distance_from_goal=self.training_get_distance_from_goal_screen.get_goal_distance()
            )
            # Connect the drill completion signal to this page so that when the drill completed, the Training Complete page can be shown
            self.training_manual_session_screen.drill_handler_thread.run_drill_signal.connect(
                self.update_main_widget_to_training_session_complete_screen)
            self.training_manual_session_screen_flows()
            self.main_widget.addWidget(self.training_manual_session_screen)
            self.main_widget.setCurrentWidget(
                self.training_manual_session_screen)
        # Otherwise, some automated session has been selected
        else:
            # If it is an automated session with the goalie profile being recorded to some drill
            if self.automated_with_goalie_session:
                # Instantiate the appropriate screen's QWidget
                self.training_automated_session_screen = screen_training_automated_session.TrainingAutomatedSessionScreen(
                    drill_name=self.training_drill_profile_selection_screen.get_selected_drill_profile(), total_ball_num=self.training_number_of_balls_selection_screen.get_session_ball_number(), distance_from_goal=self.training_get_distance_from_goal_screen.get_goal_distance(), goalie_name=self.training_goalie_profile_selection_screen.get_selected_goalie_profile())
            # Otherwise, it is an automated session without the goalie profile being recorded to some drill
            else:
                # Instantiate the appropriate screen's QWidget
                self.training_automated_session_screen = screen_training_automated_session.TrainingAutomatedSessionScreen(
                    drill_name=self.training_drill_profile_selection_screen.get_selected_drill_profile(), total_ball_num=self.training_number_of_balls_selection_screen.get_session_ball_number(), distance_from_goal=self.training_get_distance_from_goal_screen.get_goal_distance())
            # Connect the drill completion signal to this page so that when the drill completed, the Training Complete page can be shown
            self.training_automated_session_screen.drill_handler_thread.run_drill_signal.connect(
                self.update_main_widget_to_training_session_complete_screen)
            self.training_automated_session_screen_flows()
            self.main_widget.addWidget(self.training_automated_session_screen)
            self.main_widget.setCurrentWidget(
                self.training_automated_session_screen)

    @pyqtSlot(bool)
    def update_main_widget_to_training_session_complete_screen(self, some_bool):
        """update_main_widget_to_training_session_complete_screen.

        When a drill is complete in the threaded drill handler, update the Stacked Widget to display the training complete screen

        :param some_bool: Boolean object which when False means that the drill is complete
        """
        # If the drill is complete, display the training session complete page
        if not some_bool:
            self.main_widget.setCurrentWidget(
                self.training_session_complete_screen)

    def training_automated_session_screen_flows(self):
        """training_automated_session_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_automated_session_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_automated_session_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_get_distance_from_goal_screen))

    def training_manual_session_screen_flows(self):
        """training_manual_session_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_manual_session_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_manual_session_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.training_get_distance_from_goal_screen))

    def training_session_complete_screen_flows(self):
        """training_session_complete_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.training_session_complete_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))

    def profiles_screen_flows(self):
        """profiles_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.profiles_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))

        # Profiles Screen Flows
        self.profiles_screen.goalie_profiles_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.goalie_profiles_screen))
        self.profiles_screen.drill_profiles_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.drill_profiles_screen))

    def goalie_profiles_screen_flows(self):
        """goalie_profiles_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.goalie_profiles_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.goalie_profiles_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.profiles_screen))

    def drill_profiles_screen_flows(self):
        """drill_profiles_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """
        # Toolbar Flows
        self.drill_profiles_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.drill_profiles_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.profiles_screen))

    def help_screen_flows(self):
        """help_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """

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
            lambda: self.main_widget.setCurrentWidget(self.using_ball_e_help_screen))

    def calibration_help_screen_flows(self):
        """calibration_help_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """

        # Toolbar Flows
        self.calibration_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.calibration_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def training_help_screen_flows(self):
        """training_help_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """

        # Toolbar Flows
        self.training_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.training_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def profiles_help_screen_flows(self):
        """profiles_help_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """

        # Toolbar Flows
        self.profiles_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.profiles_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))

    def using_ball_e_help_screen_flows(self):
        """using_ball_e_help_screen_flows.

        This function executes all necessary setup that needs to happen in the widget. Usually it is setting the appropriate page locations in the Toolbar's buttons. If the page has other buttons, then it connects those buttons with the appropriate actions/locations.
        """

        # Toolbar Flows
        self.using_ball_e_help_screen.toolbar.back_to_home_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.home_screen))
        self.using_ball_e_help_screen.toolbar.prev_screen_button.clicked.connect(
            lambda: self.main_widget.setCurrentWidget(self.help_screen))


def main():
    """main.

    Main prototyping/testing area. Code prototyping and checking happens here. In this case, it instantiates and runs the Ball-E GUI.
    """
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
