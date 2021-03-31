import csv
import pathlib
import shutil
import sys
import threading
import time
from os import RTLD_NOW
from pathlib import Path

import pyudev
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QFileSystemWatcher, Qt, left, qChecksum, right
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QComboBox,
                             QDesktopWidget, QDialog, QHBoxLayout, QHeaderView,
                             QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QPushButton, QSizePolicy, QStackedLayout,
                             QStackedWidget, QTableWidget, QTableWidgetItem,
                             QTabWidget, QVBoxLayout, QWidget)
from pyudev.pyqt5 import MonitorObserver

import style_constants as sc
from component_button import (GenericButton, ProfileCreateButton,
                              ProfileDeleteButton)
from component_drill_creation_widget import DrillCreationWidget
from component_labels import ProfileLabel, TableHeaderLabel
from component_modal import Modal
from component_toolbar import ToolbarComponent
from helper_profiler import Profiler
from window_test import TestWindow


class TrainingSessionRecordingCheckScreen(QWidget):
    """Screen to create, delete, and view Drill Profiles

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
            self.window_title, "Back to Num. of Balls Selection")

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

        self.next_page_button = QPushButton("Next")
        self.next_page_button.setVisible(False)

        self.screen_layout.addWidget(self.next_page_button)

        # Set the screen layout
        self.setLayout(self.screen_layout)

    def check_usb_requirement(self, required_flag):

        if not required_flag:
            self.usb_connected_label.setText("You are good to go!")
            self.usb_connected_label.setVisible(True)
            self.next_page_button.setVisible(True)
        elif required_flag:
            self.yes_button.setEnabled(False)
            self.no_button.setEnabled(False)

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
        t_end = time.time() + 60
        while time.time() < t_end:
            for device in iter(self.monitor.poll, None):
                if device.action == 'add':
                    # some function to run on insertion of usb
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

        self.usb_connected_label.setVisible(False)

    def get_window_title(self):
        """Helper function to return this window's title

        Returns:
            [string]: This window's title
        """
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingSessionRecordingCheckScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
