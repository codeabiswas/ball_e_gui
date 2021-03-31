import sys

from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from component_button import GenericButton
from component_labels import ProfileLabel
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class TrainingGoalCalibrationTakePhotoScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Goal Calibration"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(
            self.window_title, "Back to Session Recording Check")

        screen_layout.addWidget(self.toolbar)

        screen_layout.addWidget(ProfileLabel(
            "Please set up the device your appropriate distance from the goal, then click Next"))

        self.next_page_button = GenericButton("Next")
        screen_layout.addWidget(self.next_page_button)

        self.setLayout(screen_layout)

        self.camera_things()

    def camera_things(self):
        cameras = QCameraInfo.availableCameras()
        for camera in cameras:
            print(camera.deviceName())

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingGoalCalibrationTakePhotoScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
