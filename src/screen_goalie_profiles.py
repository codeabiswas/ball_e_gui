import pathlib
import sys
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog,
                             QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QListWidgetItem, QPushButton, QSizePolicy,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

import style_constants as sc
from component_button import ProfileCreateButton, ProfileDeleteButton
from component_labels import ProfileLabel, TableHeaderLabel
from component_modal import Modal
from component_toolbar import ToolbarComponent
from helper_profiler import Profiler
from window_test import TestWindow


class ProfileWidget(QWidget):

    def __init__(self, text):
        super().__init__()

        self.text = text

        widget_layout = QHBoxLayout()
        widget_layout.addWidget(ProfileLabel(self.text))
        self.delete_button = ProfileDeleteButton()
        widget_layout.addWidget(self.delete_button)

        self.setLayout(widget_layout)


class GoalieProfilesScreen(QWidget):

    def __init__(self, parent=None):
        # TODO: Creating a new profile
        # TODO: Deleting a profile

        super().__init__(parent=parent)

        self.window_title = "Goalie Profiles"

        # Get the goalie profiles available on the device
        self.profiler = Profiler('goalie_profiles')
        self.goalie_profiles = self.profiler.get_profiles()

        self.screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title, "Back to Profiles")

        self.screen_layout.addWidget(self.toolbar)

        table_header_layout = QHBoxLayout()
        table_header_layout.addWidget(TableHeaderLabel('Goalie Profile Name'))
        goalie_profile_create_button = ProfileCreateButton()
        goalie_profile_create_button.clicked.connect(
            self.create_new_goalie_profile_modal)
        table_header_layout.addWidget(goalie_profile_create_button)
        self.screen_layout.addLayout(table_header_layout)

        self.scroll = QListWidget()

        for goalie_name in self.goalie_profiles.keys():
            some_goalie_profile_widget = ProfileWidget(
                goalie_name.replace('_', ' ').title())
            item = QListWidgetItem()
            self.scroll.insertItem(self.scroll.count(), item)
            self.scroll.setItemWidget(item, some_goalie_profile_widget)
            item.setSizeHint(some_goalie_profile_widget.sizeHint())

        self.scroll.itemSelectionChanged.connect(
            self.goalie_info_modal)

        self.screen_layout.addWidget(self.scroll)

        self.setLayout(self.screen_layout)

    def create_new_goalie_profile_modal(self):

        modal = QDialog()
        modal.setWindowFlags(Qt.WindowStaysOnTopHint |
                             Qt.WindowCloseButtonHint)
        modal.setWindowTitle(self.window_title)

        modal_layout = QHBoxLayout()
        modal_layout.addWidget(ProfileLabel("Name: "))
        goalie_name_input = QLineEdit()
        modal_layout.addWidget(goalie_name_input)
        new_goalie_profile_save_button = QPushButton("Save")
        new_goalie_profile_save_button.clicked.connect(
            lambda: self.create_new_goalie_profile(goalie_name_input.text()))
        modal_layout.addWidget(new_goalie_profile_save_button)

        modal.setLayout(modal_layout)

        modal.exec_()

    def create_new_goalie_profile(self, goalie_name):
        location = str(Path.home()) + \
            '/Documents/ball_e_profiles/goalie_profiles/' + \
            goalie_name.replace(' ', '_').lower()
        pathlib.Path(location).mkdir(parents=True, exist_ok=True)
        pathlib.Path(location+'/{}.csv'.format(goalie_name.replace(' ',
                                                                   '_').lower())).touch(exist_ok=True)

    def goalie_info_modal(self):

        selected_data = self.scroll.selectedIndexes()[0]

        goalie_name = list(self.goalie_profiles.keys())[
            selected_data.row()]
        goalie_profile_path = self.goalie_profiles[goalie_name]

        modal_layout = QVBoxLayout()

        modal_layout.addWidget(ProfileLabel(
            'Name: {}'.format(goalie_name.replace('_', ' ').title())))

        table_view = QTableWidget()
        table_view.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        goalie_info = self.profiler.get_profile_info(goalie_profile_path)

        counter = 0
        table_view.setRowCount(len(goalie_info))
        table_view.setColumnCount(2)
        for drill_info, date_info in zip(goalie_info.keys(), goalie_info.values()):
            drill_name_widget = QTableWidgetItem(drill_info)
            date_info_widget = QTableWidgetItem(date_info)
            some_font = QFont()
            some_font.setPixelSize(int(sc.FONT_M[:2]))
            drill_name_widget.setFont(some_font)
            date_info_widget.setFont(some_font)
            drill_name_widget.setTextAlignment(Qt.AlignCenter)
            date_info_widget.setTextAlignment(Qt.AlignCenter)
            table_view.setItem(counter, 0, drill_name_widget)
            table_view.setItem(counter, 1, date_info_widget)
            counter += 1
        table_view.setHorizontalHeaderLabels(
            ["Drill History", "Date Performed"])
        table_view.verticalHeader().setVisible(False)

        table_view.horizontalHeader().setStyleSheet(
            """
            font-size: {font_size}
            """.format(font_size=sc.FONT_M)
        )

        table_view.verticalHeader().setStyleSheet(
            """
            font-size: {font_size}
            """.format(font_size=sc.FONT_M)
        )

        table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        modal_layout.addWidget(table_view)

        Modal(
            type="info",
            layout=modal_layout,
            window_title=self.get_window_title()
        )

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(GoalieProfilesScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
