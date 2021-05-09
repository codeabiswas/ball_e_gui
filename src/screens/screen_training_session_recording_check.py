"""
screen_training_session_recording_check.py
---
This file contains the TrainingSessionRecordingCheckScreen class, which is displayed when the user is to select whether to record the training session or not.
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
    from component_labels import ProfileLabel
    from component_toolbar import ToolbarComponent
    from window_test import TestWindow
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    import functools

    import pyudev
    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget
    from pyudev.pyqt5 import MonitorObserver


class TrainingSessionRecordingCheckScreen(QWidget):
    """This class instantiates the screen which allows the user to select whether or not they want to record the screen, which is when the USB insertion flow is instantiated.

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self):
        """Widget Initialization
        """

        super().__init__()

        self.window_title = "Session Recording Check"

        # Create a screen layout object to populate
        self.screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(
            self.window_title, "Back to # of Balls\n Select")

        self.screen_layout.addWidget(self.toolbar)

        self.screen_layout.addWidget(ProfileLabel(
            "Record Session?"))

        self.button_container_layout = QHBoxLayout()

        self.yes_button = GenericButton("Yes")
        self.yes_button.clicked.connect(
            lambda: self.check_usb_requirement(True))
        self.button_container_layout.addWidget(self.yes_button)
        self.no_button = GenericButton("No")
        self.no_button.clicked.connect(
            lambda: self.check_usb_requirement(False))
        self.button_container_layout.addWidget(self.no_button)

        self.screen_layout.addLayout(self.button_container_layout)

        self.usb_connected_label = ProfileLabel("")
        self.usb_connected_label.setVisible(False)
        self.screen_layout.addWidget(self.usb_connected_label)

        self.next_page_button = GenericButton("Next")
        self.next_page_button.setVisible(False)

        self.screen_layout.addWidget(self.next_page_button)

        # Set the screen layout
        self.setLayout(self.screen_layout)

    def check_usb_requirement(self, required_flag):
        """check_usb_requirement.

        This function asks the user to insert a USB if they want to record a training session. Otherwise, the user is allowed to proceed

        :param required_flag: Boolean value which when True ensures that the user goes through the flow to insert a USB.
        """

        # the training session is not being recorded - no USB required
        if not required_flag:
            self.usb_connected_label.setText("You are good to go!")
            self.usb_connected_label.setVisible(True)
            self.next_page_button.setVisible(True)
        # The training session is being recorded - USB required
        elif required_flag:
            self.yes_button.setEnabled(False)
            self.no_button.setEnabled(False)
            self.next_page_button.setVisible(False)

            self.usb_connected_label.setText(
                "Please insert USB now")
            self.usb_connected_label.setVisible(True)

            self.context = pyudev.Context()
            self.monitor = pyudev.Monitor.from_netlink(self.context)
            self.monitor.filter_by(subsystem='usb')
            self.observer = MonitorObserver(self.monitor)
            self.observer.deviceEvent.connect(self.find_usb)
            self.monitor.start()

    def find_usb(self):
        """find_usb.

        This function polls and locates the USB that the user has inserted within 60 seconds
        """

        # t_end = time.time() + 60
        # while time.time() < t_end:
        # device = self.monitor.poll(timeout=60)
        for device in iter(functools.partial(self.monitor.poll(timeout=60)), None):
            if device.action == 'add':
                # some function to run on insertion of usb
                print(device.device_path)
                self.usb_connected_label.setText("You are good to go!")
                self.usb_connected_label.setVisible(True)
                self.next_page_button.setVisible(True)
                self.yes_button.setEnabled(True)
                self.no_button.setEnabled(True)
                return
        self.usb_connected_label.setText(
            "No USB detected. To try again, please select the Yes Button and follow the steps.")
        self.usb_connected_label.setVisible(True)
        self.next_page_button.setVisible(False)
        self.yes_button.setEnabled(True)
        self.no_button.setEnabled(True)

    def reset_screen(self):
        """reset_screen.

        This function resets the screen so that it can be used in the future.
        """

        self.usb_connected_label.setVisible(False)

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
    win = TestWindow(TrainingSessionRecordingCheckScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
