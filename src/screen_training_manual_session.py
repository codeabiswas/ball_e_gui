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


class TrainingManualSessionScreen(QWidget):
    """Screen to create, delete, and view Drill Profiles

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self, total_ball_num):
        """Widget Initialization
        """
        super().__init__()

        self.window_title = "Manual Training Session"

        self.curr_ball_num = 1
        self.total_ball_num = total_ball_num

        # Create a screen layout object to populate
        self.screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(
            self.window_title, "Back to Goal Calibration")

        self.screen_layout.addWidget(self.toolbar)

        self.row_layout = QHBoxLayout()

        self.ball_number_label = ProfileLabel(
            "Ball {} out of {}".format(self.curr_ball_num, self.total_ball_num))
        self.row_layout.addWidget(self.ball_number_label)

        self.column_layout = QVBoxLayout()
        self.shot_location_label = ProfileLabel("")
        self.column_layout.addWidget(self.shot_location_label)

        self.lax_goal_label = QLabel()
        self.lax_goal_image_setup()
        self.column_layout.addWidget(self.lax_goal_label)

        self.row_layout.addLayout(self.column_layout)

        self.shoot_button = GenericButton("Shoot")
        self.shoot_button.clicked.connect(self.shoot_button_clicked)
        self.row_layout.addWidget(self.shoot_button)

        self.screen_layout.addLayout(self.row_layout)

        # Set the screen layout
        self.setLayout(self.screen_layout)

    def lax_goal_image_setup(self):

        lax_goal_img_location = str(
            Path.home()) + '/Developer/ball_e_gui/src/images/lax_goal.png'
        pixmap_object = QPixmap()
        pixmap_object.load(lax_goal_img_location)
        self.scaled_pixmap_obj = pixmap_object.scaled(pixmap_object.width()-300,
                                                      pixmap_object.height()-300)
        self.lax_goal_label.mousePressEvent = self.show_shot_location

        painter_obj = QPainter(self.scaled_pixmap_obj)
        painter_obj.setPen(QPen(Qt.green, 12, Qt.SolidLine))

        # Top Line
        painter_obj.drawLine(0, 0, self.scaled_pixmap_obj.width(), 0)
        # Top 1/3 Line
        painter_obj.drawLine(0, int(self.scaled_pixmap_obj.height(
        )/3), self.scaled_pixmap_obj.width(), int(self.scaled_pixmap_obj.height()/3))
        # Bottom 1/3 Line
        painter_obj.drawLine(0, (self.scaled_pixmap_obj.height() - int(self.scaled_pixmap_obj.height()/3)),
                             self.scaled_pixmap_obj.width(), (self.scaled_pixmap_obj.height() - int(self.scaled_pixmap_obj.height()/3)))
        # Bottom Line
        painter_obj.drawLine(0, self.scaled_pixmap_obj.height(),
                             self.scaled_pixmap_obj.width(), self.scaled_pixmap_obj.height())
        # Left Line
        painter_obj.drawLine(0, 0,
                             0, self.scaled_pixmap_obj.height())
        # Left 1/3 Line
        painter_obj.drawLine(int(self.scaled_pixmap_obj.width(
        )/3), 0, int(self.scaled_pixmap_obj.width(
        )/3), self.scaled_pixmap_obj.height())
        # Right 1/3 Line
        painter_obj.drawLine(int(self.scaled_pixmap_obj.width() - self.scaled_pixmap_obj.width()/3), 0,
                             int(self.scaled_pixmap_obj.width() - self.scaled_pixmap_obj.width()/3), self.scaled_pixmap_obj.height())
        # Right Line
        painter_obj.drawLine(self.scaled_pixmap_obj.width(), 0,
                             self.scaled_pixmap_obj.width(), self.scaled_pixmap_obj.height())

        painter_obj.end()

        self.lax_goal_label.setPixmap(self.scaled_pixmap_obj)

    def show_shot_location(self, event):
        x_coord = event.pos().x()
        y_coord = event.pos().y()

        third_of_height = int(self.scaled_pixmap_obj.height()/3)
        two_third_of_height = self.scaled_pixmap_obj.height() - third_of_height

        third_of_width = int(self.scaled_pixmap_obj.width()/3)
        two_third_of_width = self.scaled_pixmap_obj.width() - third_of_width

        top_flag = False
        bottom_flag = False
        center_flag = False
        left_flag = False
        right_flag = False
        middle_flag = False

        if y_coord < third_of_height:
            top_flag = True
        elif y_coord > two_third_of_height:
            bottom_flag = True
        elif y_coord >= third_of_height and y_coord <= two_third_of_height:
            center_flag = True

        if x_coord < third_of_width:
            left_flag = True
        elif x_coord > two_third_of_width:
            right_flag = True
        elif x_coord >= third_of_width and x_coord <= two_third_of_width:
            middle_flag = True

        if top_flag and left_flag:
            self.shot_location_label.setText(
                "Shot Location: Top Left")
        elif top_flag and right_flag:
            self.shot_location_label.setText(
                "Shot Location: Top Right")
        elif top_flag and middle_flag:
            self.shot_location_label.setText(
                "Shot Location: Top Middle")
        elif center_flag and left_flag:
            self.shot_location_label.setText(
                "Shot Location: Center Left")
        elif center_flag and right_flag:
            self.shot_location_label.setText(
                "Shot Location: Center Right")
        elif center_flag and middle_flag:
            self.shot_location_label.setText(
                "Shot Location: Center Middle")
        elif bottom_flag and left_flag:
            self.shot_location_label.setText(
                "Shot Location: Bottom Left")
        elif bottom_flag and right_flag:
            self.shot_location_label.setText(
                "Shot Location: Bottom Right")
        elif bottom_flag and middle_flag:
            self.shot_location_label.setText(
                "Shot Location: Bottom Middle")

    def shoot_button_clicked(self):
        self.curr_ball_num += 1
        self.ball_number_label.setText("Ball {} out of {}".format(
            self.curr_ball_num, self.total_ball_num))

    def get_window_title(self):
        """Helper function to return this window's title

        Returns:
            [string]: This window's title
        """
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingManualSessionScreen(5))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
