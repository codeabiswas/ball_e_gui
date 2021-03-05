import os
import sys
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListView,
                             QListWidget, QListWidgetItem, QMessageBox,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

import helper_doc_reader as hdr
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class ProfileLabel(QLabel):
    def __init__(self, profile_label):
        super().__init__()
        self.setText(profile_label)
        self.setStyleSheet(
            """
            color: black;
            font-size: 20px;
            """
        )


class ProfileCreateButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Create New")
        self.setFixedWidth(150)
        self.setStyleSheet(
            """
            background-color: green;
            color: white;
            font-size: 16px;
            font-weight: bold;
            """
        )


class ProfileDeleteButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Delete")
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding
        )
        self.setFixedWidth(100)
        self.setStyleSheet(
            """
            background-color: red;
            color: white;
            font-size: 16px;
            font-weight: bold;
            """
        )


class ProfileWidget(QWidget):

    def __init__(self, text):
        super().__init__()

        self.text = text

        widget_layout = QHBoxLayout()
        widget_layout.addWidget(ProfileLabel(self.text))
        self.delete_button = ProfileDeleteButton()
        widget_layout.addWidget(self.delete_button)

        self.setLayout(widget_layout)


class TableHeaderLabel(QLabel):
    def __init__(self, table_header_label):
        super().__init__()
        self.setText(table_header_label)
        self.setStyleSheet(
            """
            color: black;
            font-size: 26px;
            font-weight: bold;
            """
        )


class Profiler():
    def __init__(self, dirname):
        self.dirname = dirname

    def get_profiles(self):

        location = str(Path.home()) + \
            '/Documents/ball_e_profiles/' + self.dirname
        profile_names = list()
        profile_info = list()
        for r, profile_dirs, profile_infos in os.walk(location):
            for profile_dir in profile_dirs:
                profile_names.append(profile_dir)
            for each_profile_info in profile_infos:
                profile_info.append(os.path.join(r, each_profile_info))

        return {profile_names[i]: profile_info[i] for i in range(len(profile_names))}

    def get_profile_info(self, profile_name):
        pass


class GoalieProfilesScreen(QWidget):

    def __init__(self, parent=None):
        # TODO: Creating a new profile
        # TODO: Deleted a profile

        super().__init__(parent=parent)

        self.window_title = "Goalie Profiles"

        # Get the goalie profiles available on the device
        profiler = Profiler('goalie_profiles')
        self.goalie_profiles = profiler.get_profiles()

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title, "Back to Profiles")

        screen_layout.addWidget(self.toolbar)

        table_header_layout = QHBoxLayout()
        table_header_layout.addWidget(TableHeaderLabel('Goalie Profile Name'))
        table_header_layout.addWidget(ProfileCreateButton())
        screen_layout.addLayout(table_header_layout)

        self.scroll = QListWidget()

        for goalie_name in self.goalie_profiles.keys():
            some_goalie_profile_widget = ProfileWidget(
                goalie_name.replace('_', ' ').title())
            item = QListWidgetItem()
            self.scroll.insertItem(self.scroll.count(), item)
            self.scroll.setItemWidget(item, some_goalie_profile_widget)
            item.setSizeHint(some_goalie_profile_widget.sizeHint())

        self.scroll.itemSelectionChanged.connect(self.pop_up_generator)

        screen_layout.addWidget(self.scroll)

        self.setLayout(screen_layout)

    def pop_up_generator(self):
        # TODO: Create a scroll view of the Goalie Profile

        selected_data = self.scroll.selectedIndexes()[0]

        pop_up = QMessageBox()
        pop_up.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        pop_up.setWindowTitle(self.window_title)
        pop_up.setStandardButtons(QMessageBox.Close)

        goalie_name = list(self.goalie_profiles.keys())[
            selected_data.row()]
        goalie_profile_path = self.goalie_profiles[goalie_name]
        pop_up.setText('Goalie Name: {}'.format(
            goalie_name.replace('_', ' ').title()))
        pop_up.setInformativeText(goalie_profile_path)

        pop_up.setStyleSheet(
            """
            font-size: 22px;
            """
        )

        pop_up.exec_()

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(GoalieProfilesScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
