"""
screen_training_goalie_profile_selection.py
---
This file contains the TrainingGoalieProfileSelectionScreen class, which is where the user selects the Goalie Profile for an Automated Training Session.
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
    from helper_profiler import Profiler
    from window_test import TestWindow

except ImportError:
    print("{}: Imports failed".format(__file__))
finally:

    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QHeaderView,
                                 QSizePolicy, QTableWidget, QTableWidgetItem,
                                 QVBoxLayout, QWidget)


class TrainingGoalieProfileSelectionScreen(QWidget):
    """TrainingGoalieProfileSelectionScreen.

    This class instantiates the QWidget object for allowing the user to pick a Goalie for an Automated Training Session.
    """

    def __init__(self, parent=None):
        """__init__.

        Widget initialization
        """

        super().__init__(parent=parent)

        self.window_title = "Goalie Profile Selection"

        self.profiler = Profiler('goalie_profiles')
        self.goalie_profiles = self.profiler.get_profiles()

        self.selected_goalie_profile = None

        # This font will be used for all table related purposes
        self.table_font = QFont()
        self.table_font.setPixelSize(int(sc.FONT_L[:2]))

        self.screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title, "Back to Training")

        self.screen_layout.addWidget(self.toolbar)

        screen_layout_row_one = QHBoxLayout()

        self.goalie_profile_selection_label = ProfileLabel(
            "Please Select a Goalie Profile to Continue")
        screen_layout_row_one.addWidget(self.goalie_profile_selection_label)

        self.next_page_button = GenericButton("Next")
        self.next_page_button.setVisible(False)
        screen_layout_row_one.addWidget(self.next_page_button)
        self.screen_layout.addLayout(screen_layout_row_one)

        self.create_table_header_view(
            table_title_name="Goalie Profiles", header_clicked_action=self.unselect_table_header)
        self.table_header.resizeRowsToContents()
        self.screen_layout.addWidget(self.table_header)

        # Create the main table and add to the layout
        self.create_main_table_view(profile_dict_obj=self.goalie_profiles,
                                    table_clicked_action=self.choose_main_table_click_action)
        self.main_table_view.resizeRowsToContents()
        self.screen_layout.addWidget(self.main_table_view)

        self.setLayout(self.screen_layout)

    def update_profiles(self):
        """Refreshes the profiles on the screen to show to the user
        """
        self.screen_layout.removeWidget(self.main_table_view)

        self.goalie_profiles = self.profiler.get_profiles()

        # Create the main table and add to the layout
        self.create_main_table_view(profile_dict_obj=self.goalie_profiles,
                                    table_clicked_action=self.choose_main_table_click_action)
        self.main_table_view.resizeRowsToContents()
        self.screen_layout.addWidget(self.main_table_view)

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
        self.table_header.setFixedHeight(
            int(self.table_header.sizeHint().height()/2))

    def unselect_table_header(self):
        """unselect_table_header.

        This function deselects whatever has been clicked on the table header so that it does not look odd.
        """

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
        """choose_main_table_click_action.

        This function is the main action that occurs after one of the table's cells has been clicked

        :param item: The object that was clicked in the table
        """

        goalie_name = self.main_table_view.item(item.row(), 0).text()

        self.goalie_profile_selection_label.setText("You have selected: {}".format(
            goalie_name
        ))
        self.next_page_button.setVisible(True)

        self.selected_goalie_profile = goalie_name.replace(' ', '_').lower()

    def reset_screen(self):
        """reset_screen.

        This function resets the page accordingly so that it can be used again in the future
        """

        # Unselect the currently picked cell
        self.main_table_view.selectedItems()[
            0].setSelected(False)

        self.goalie_profile_selection_label.setText(
            "Please Select a Goalie Profile to Continue")

    def get_selected_goalie_profile(self):
        """get_selected_goalie_profile.

        This function returns which goalie profile is currently selected.
        """

        return self.selected_goalie_profile

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
    win = TestWindow(TrainingGoalieProfileSelectionScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Run the main function
    main()
