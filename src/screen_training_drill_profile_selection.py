import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
                             QMainWindow, QPushButton, QSizePolicy,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

import style_constants as sc
from component_button import GenericButton
from component_labels import ProfileLabel
from component_toolbar import ToolbarComponent
from helper_profiler import Profiler
from window_test import TestWindow


class TrainingDrillProfileSelectionScreen(QWidget):
    def __init__(self, selected_goalie_profile=None):
        super().__init__()

        self.window_title = "Drill Profile Selection"

        self.profiler = Profiler('drill_profiles')
        self.drill_profiles = self.profiler.get_profiles()

        self.selected_drill_profile = None

        # This font will be used for all table related purposes
        self.table_font = QFont()
        self.table_font.setPixelSize(int(sc.FONT_M[:2]))

        screen_layout = QVBoxLayout()

        if selected_goalie_profile is None:
            self.toolbar = ToolbarComponent(
                self.window_title, "Back to Training")
        else:
            self.toolbar = ToolbarComponent(
                self.window_title, "Back to Goalie Profile Selection")

        # TODO: Continue from here
        screen_layout.addWidget(self.toolbar)

        screen_layout_row_one = QHBoxLayout()

        self.goalie_profile_selection_label = ProfileLabel(
            "Please Select a Goalie Profile to Continue")
        screen_layout_row_one.addWidget(self.goalie_profile_selection_label)

        self.next_page_button = QPushButton("Next")
        self.next_page_button.setVisible(False)
        screen_layout_row_one.addWidget(self.next_page_button)
        screen_layout.addLayout(screen_layout_row_one)

        self.create_table_header_view(
            table_title_name="Goalie Profiles", header_clicked_action=self.unselect_table_header)
        screen_layout.addWidget(self.table_header)

        # Create the main table and add to the layout
        self.create_main_table_view(profile_dict_obj=self.drill_profiles,
                                    table_clicked_action=self.choose_main_table_click_action)
        screen_layout.addWidget(self.main_table_view)

        self.setLayout(screen_layout)

    def create_table_header_view(self, table_title_name, header_clicked_action):
        """Creates a table header for the table below it

        Args:
            table_title_name (str): Table's title
        """

        # Create the table object that acts as the "header" for the main goalie profile table view
        self.table_header = QTableWidget()
        # Do not allow the user to edit the content of the table
        self.table_header.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)
        # Set the number of rows and columns of this table. Since it is a header, only 1 row.
        self.table_header.setRowCount(1)
        self.table_header.setColumnCount(1)

        # Create a table title cell and set it in the right section
        table_title_widget = QTableWidgetItem(table_title_name)
        table_title_widget.setFont(self.table_font)
        self.table_header.setItem(
            0, 0, table_title_widget
        )

        # Function to execute when a cell from this header is clicked
        self.table_header.clicked.connect(header_clicked_action)

        # Capture the horizontal header of this table
        header_hor_head = self.table_header.horizontalHeader()

        # Hide all headers of the table
        self.table_header.verticalHeader().setVisible(False)
        header_hor_head.setVisible(False)

        # Size the header appropriately
        header_hor_head.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_header.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Fixed
        )
        self.table_header.setFixedHeight(sc.TABLE_HEADER_HEIGHT)

    def unselect_table_header(self):
        # Unselect the currently picked cell
        self.table_header.selectedItems()[0].setSelected(False)

    def create_main_table_view(self, profile_dict_obj, table_clicked_action):
        """Creates the main table widget from a profile dictionary

        Args:
            profile_dict_obj (dict): Dictionary that contains the profile info (the profile name and its path)
            table_clicked_action (function): Function to execute when table is clicked
        """

        # Create the main table widget where data will be populated
        self.main_table_view = QTableWidget()
        # Do not allow the user to edit the contents of the table
        self.main_table_view.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)
        # The number of rows is defined by how many objects there are in the dictionary
        self.main_table_view.setRowCount(len(profile_dict_obj))
        self.main_table_view.setColumnCount(1)

        # Iterate through the data in the dictionary and format it appropriately in the table
        for row_count, profile_name in enumerate(profile_dict_obj):
            # Modify the profile name's string and populate into a table cell
            mod_profile_name = profile_name.replace('_', ' ').title()
            mod_profile_name_widget = QTableWidgetItem(mod_profile_name)
            mod_profile_name_widget.setFont(self.table_font)
            # Align items in their respective cells appropriately
            mod_profile_name_widget.setTextAlignment(Qt.AlignLeft)
            # Add items to the table view
            self.main_table_view.setItem(
                row_count, 0, mod_profile_name_widget)

        # Function to execute when a cell from this table is clicked
        self.main_table_view.clicked.connect(table_clicked_action)

        # Capture the horizontal header of the table
        main_table_hor_head = self.main_table_view.horizontalHeader()

        # Hide all headers of the table
        self.main_table_view.verticalHeader().setVisible(False)
        main_table_hor_head.setVisible(False)

        # Resize the left column to stretch as far out as possible
        main_table_hor_head.setSectionResizeMode(0, QHeaderView.Stretch)

    def choose_main_table_click_action(self, item):
        goalie_name = self.main_table_view.item(item.row(), 0).text()

        self.goalie_profile_selection_label.setText("You have selected: {}".format(
            goalie_name
        ))
        self.next_page_button.setVisible(True)

        self.selected_drill_profile = goalie_name.replace(' ', '_').lower()

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingGoalieProfileSelectionScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
