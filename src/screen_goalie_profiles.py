import pathlib
import shutil
import sys
from os import RTLD_NOW
from pathlib import Path

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, qChecksum
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDesktopWidget,
                             QDialog, QHBoxLayout, QHeaderView, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QPushButton, QSizePolicy, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

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
        self.curr_goalie_profiles_len = len(self.goalie_profiles)

        self.screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title, "Back to Profiles")

        self.screen_layout.addWidget(self.toolbar)

        self.table_header = QTableWidget()
        self.table_header.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)
        self.table_header.setRowCount(1)
        self.table_header.setColumnCount(2)

        table_title_widget = QTableWidgetItem("Goalie Profile Names")

        some_font = QFont()
        some_font.setPixelSize(int(sc.FONT_M[:2]))
        table_title_widget.setFont(some_font)
        self.table_header.setItem(
            0, 0, table_title_widget
        )

        create_new_goalie_profile_widget = QTableWidgetItem(
            "Create New")
        create_new_goalie_profile_widget.setFont(some_font)
        self.table_header.setItem(
            0, 1, create_new_goalie_profile_widget
        )

        self.table_header.clicked.connect(
            self.create_new_goalie_profile_modal)

        self.table_header.verticalHeader().setVisible(False)
        self.table_header.horizontalHeader().setVisible(False)

        self.table_header.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_header.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents)
        self.table_header.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Fixed
        )
        self.table_header.setFixedHeight(sc.TABLE_HEADER_HEIGHT)

        self.screen_layout.addWidget(self.table_header)

        self.scroll = QTableWidget()
        self.scroll.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.scroll.setRowCount(len(self.goalie_profiles))
        self.scroll.setColumnCount(2)

        for row_count, goalie_name in enumerate(self.goalie_profiles.keys()):
            mod_goalie_name = goalie_name.replace('_', ' ').title()
            mod_goalie_name_widget = QTableWidgetItem(mod_goalie_name)
            delete_row_widget = QTableWidgetItem('Delete')
            delete_row_widget.setBackground(
                QColor(sc.COLOR_ERROR)
            )
            delete_row_widget.setForeground(
                QColor(sc.COLOR_WHITE)
            )
            some_font = QFont()
            some_font.setPixelSize(int(sc.FONT_M[:2]))
            mod_goalie_name_widget.setFont(some_font)
            delete_row_widget.setFont(some_font)
            mod_goalie_name_widget.setTextAlignment(Qt.AlignLeft)
            delete_row_widget.setTextAlignment(Qt.AlignRight)
            self.scroll.setItem(
                row_count, 0, mod_goalie_name_widget)
            self.scroll.setItem(
                row_count, 1, delete_row_widget)
        self.scroll.clicked.connect(self.choose_table_click_action)

        self.scroll.verticalHeader().setVisible(False)
        self.scroll.horizontalHeader().setVisible(False)

        self.scroll.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.scroll.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents)

        self.screen_layout.addWidget(self.scroll)

        self.setLayout(self.screen_layout)

    def choose_table_click_action(self, item):
        selected_item = self.scroll.selectedItems()[0]
        selected_item.setSelected(False)

        if item.column() == 0:
            self.goalie_info_modal(item.row())
        elif item.column() == 1:

            check_delete_modal_layout = QVBoxLayout()
            check_delete_modal_layout.addWidget(
                QLabel("Are you sure you want to delete this goalie profile?"))
            check_delete_modal = Modal(
                type="choice",
                layout=check_delete_modal_layout,
                window_title=self.scroll.item(item.row(), 0).text()

            )

            check_delete_modal.yes_button.clicked.connect(
                lambda: self.remove_goalie_profile(item.row(), check_delete_modal))

            check_delete_modal.exec_()

    def remove_goalie_profile(self, table_row, modal_object):

        location = str(Path.home()) + '/Documents/ball_e_profiles/goalie_profiles/' + \
            self.scroll.item(table_row, 0).text().replace(' ', '_').lower()
        shutil.rmtree(location, ignore_errors=True)
        self.scroll.removeRow(table_row)

        self.goalie_profiles = self.profiler.get_profiles()
        self.curr_goalie_profiles_len = len(self.goalie_profiles)

        modal_object.close()

    def create_new_goalie_profile_modal(self, item):

        selected_item = self.table_header.selectedItems()[0]
        selected_item.setSelected(False)

        if item.column() == 1:

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
        location = str(Path.home()) + '/Documents/ball_e_profiles/goalie_profiles/' + \
            goalie_name.replace(' ', '_').lower()
        try:
            pathlib.Path(location).mkdir(parents=True, exist_ok=False)
            pathlib.Path(location+'/{}.csv'.format(goalie_name.replace(' ',
                                                                       '_').lower())).touch(exist_ok=False)
            last_row_num = self.scroll.rowCount()
            self.scroll.insertRow(last_row_num)

            mod_goalie_name_widget = QTableWidgetItem(goalie_name)
            delete_row_widget = QTableWidgetItem('Delete')
            delete_row_widget.setBackground(
                QColor(sc.COLOR_ERROR)
            )
            delete_row_widget.setForeground(
                QColor(sc.COLOR_WHITE)
            )
            some_font = QFont()
            some_font.setPixelSize(int(sc.FONT_M[:2]))
            mod_goalie_name_widget.setFont(some_font)
            delete_row_widget.setFont(some_font)
            mod_goalie_name_widget.setTextAlignment(Qt.AlignLeft)
            delete_row_widget.setTextAlignment(Qt.AlignRight)
            self.scroll.setItem(
                last_row_num, 0, mod_goalie_name_widget)
            self.scroll.setItem(
                last_row_num, 1, delete_row_widget)

            self.goalie_profiles = self.profiler.get_profiles()
            self.curr_goalie_profiles_len = len(self.goalie_profiles)

        except FileExistsError:
            error_modal_layout = QVBoxLayout()
            error_modal_layout.addWidget(QLabel("Goalie Exists"))
            Modal(
                type="error",
                layout=error_modal_layout,
                window_title=self.get_window_title()
            )

    def goalie_info_modal(self, table_row):

        if table_row >= self.curr_goalie_profiles_len:
            info_modal_layout = QVBoxLayout()
            info_modal_layout.addWidget(QLabel("No information yet."))
            Modal(
                type="info",
                layout=info_modal_layout,
                window_title=self.scroll.item(table_row, 0).text()
            )
            return

        goalie_name = self.scroll.item(
            table_row, 0).text().replace(' ', '_').lower()
        goalie_profile_path = self.goalie_profiles[goalie_name]

        modal_layout = QVBoxLayout()

        table_view = QTableWidget()
        table_view.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        goalie_info = self.profiler.get_profile_info(goalie_profile_path)

        if(len(goalie_info) == 0):
            info_modal_layout = QVBoxLayout()
            info_modal_layout.addWidget(QLabel("No information yet."))
            Modal(
                type="info",
                layout=info_modal_layout,
                window_title=goalie_name.replace('_', ' ').title()
            )
            return

        table_view.setRowCount(len(goalie_info))
        table_view.setColumnCount(2)

        for curr_row, (drill_info, date_info) in enumerate(zip(goalie_info.keys(), goalie_info.values())):
            drill_name_widget = QTableWidgetItem(drill_info)
            date_info_widget = QTableWidgetItem(date_info)
            some_font = QFont()
            some_font.setPixelSize(int(sc.FONT_M[:2]))
            drill_name_widget.setFont(some_font)
            date_info_widget.setFont(some_font)
            drill_name_widget.setTextAlignment(Qt.AlignCenter)
            date_info_widget.setTextAlignment(Qt.AlignCenter)
            table_view.setItem(curr_row, 0, drill_name_widget)
            table_view.setItem(curr_row, 1, date_info_widget)

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
            window_title=goalie_name.replace('_', ' ').title()
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
