import sys

import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

import style_constants as sc
from component_button import GenericButton
from component_labels import ProfileLabel
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def gstreamer_pipeline(
        self,
        capture_width=1280,
        capture_height=720,
        display_width=1280,
        display_height=720,
        framerate=60,
        flip_method=0,
    ):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )


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

        # Image frames shown in this
        self.image_label = QLabel()
        screen_layout.addWidget(self.image_label)

        self.next_page_button = GenericButton("Next")
        screen_layout.addWidget(self.next_page_button)

        self.setLayout(screen_layout)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def get_window_title(self):
        return self.window_title

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingGoalCalibrationTakePhotoScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
