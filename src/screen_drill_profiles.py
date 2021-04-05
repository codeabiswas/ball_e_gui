import csv
import pathlib
import shutil
import sys
from os import RTLD_NOW
from pathlib import Path

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, left, qChecksum, right
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QComboBox,
                             QDesktopWidget, QDialog, QHBoxLayout, QHeaderView,
                             QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QPushButton, QSizePolicy, QStackedLayout,
                             QStackedWidget, QTableWidget, QTableWidgetItem,
                             QTabWidget, QVBoxLayout, QWidget)

import style_constants as sc
from component_button import (GenericButton, ProfileCreateButton,
                              ProfileDeleteButton)
from component_drill_creation_widget import DrillCreationWidget
from component_dropdown import Dropdown
from component_labels import ProfileLabel, TableHeaderLabel
from component_lineedit import LineEdit
from component_modal import Modal
from component_toolbar import ToolbarComponent
from helper_profiler import Profiler
from window_test import TestWindow


class DrillProfilesScreen(QWidget):
    """Screen to create, delete, and view Drill Profiles

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self):
        """Widget Initialization
        """
        super().__init__()

        self.window_title = "Drill Profiles"

        # Get the drill profiles available on the device
        self.profiler = Profiler('drill_profiles')
        self.get_drill_profiles_info()

        # The minimum number of balls required to create any drills
        self.curr_drill_balls = 1

        # The minimum ROF for any drill
        self.curr_drill_rof = sc.MIN_ROF

        # This font will be used for all table related purposes
        self.table_font = QFont()
        self.table_font.setPixelSize(int(sc.FONT_L[:2]))

        # Create a screen layout object to populate
        self.screen_layout = QVBoxLayout()

        # Create a toolback object and add it to the top of the layout
        self.toolbar = ToolbarComponent(self.window_title, "Back to Profiles")
        self.screen_layout.addWidget(self.toolbar)

        # Create a table header and add to the layout
        self.create_table_header_view(
            table_title_name="Drill Profiles",
            header_clicked_action=self.create_new_drill_profile_modal_page_one)
        self.screen_layout.addWidget(self.table_header)

        # Create the main table and add to the layout
        self.create_main_table_view(profile_dict_obj=self.drill_profiles,
                                    table_clicked_action=self.choose_main_table_click_action)
        self.screen_layout.addWidget(self.main_table_view)

        # Set the screen layout
        self.setLayout(self.screen_layout)

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
        # 2 columns: one for the profile name and one for the delete button
        self.main_table_view.setColumnCount(2)

        # Iterate through the data in the dictionary and format it appropriately in the table
        for row_count, profile_name in enumerate(profile_dict_obj):
            # Modify the profile name's string and populate into a table cell
            mod_profile_name = profile_name.replace('_', ' ').title()
            mod_profile_name_widget = QTableWidgetItem(mod_profile_name)
            # Create a delete 'button' by converting a cell to act like a button
            delete_row_widget = QTableWidgetItem('Delete')
            delete_row_widget.setBackground(
                QColor(sc.COLOR_ERROR)
            )
            delete_row_widget.setForeground(
                QColor(sc.COLOR_WHITE)
            )
            mod_profile_name_widget.setFont(self.table_font)
            delete_row_widget.setFont(self.table_font)
            # Align items in their respective cells appropriately
            mod_profile_name_widget.setTextAlignment(Qt.AlignLeft)
            delete_row_widget.setTextAlignment(Qt.AlignRight)
            # Add items to the table view
            self.main_table_view.setItem(
                row_count, 0, mod_profile_name_widget)
            self.main_table_view.setItem(
                row_count, 1, delete_row_widget)

        # Function to execute when a cell from this table is clicked
        self.main_table_view.clicked.connect(table_clicked_action)

        # Capture the horizontal header of the table
        main_table_hor_head = self.main_table_view.horizontalHeader()

        # Hide all headers of the table
        self.main_table_view.verticalHeader().setVisible(False)
        main_table_hor_head.setVisible(False)

        # Resize the left column to stretch as far out as possible
        main_table_hor_head.setSectionResizeMode(0, QHeaderView.Stretch)
        # Resize the right column to wrap around its contents
        main_table_hor_head.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)
        self.main_table_view.resizeRowsToContents()

    def create_table_header_view(self, table_title_name, header_clicked_action):
        """Creates a table header for the table below it

        Args:
            table_title_name (str): Table's title
            header_clicked (function): Function to execute when the header is clicked
        """

        # Create the table object that acts as the "header" for the main drill profile table view
        self.table_header = QTableWidget()
        # Do not allow the user to edit the content of the table
        self.table_header.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)
        # Set the number of rows and columns of this table. Since it is a header, only 1 row.
        self.table_header.setRowCount(1)
        self.table_header.setColumnCount(2)

        # Create a table title cell and set it in the right section
        table_title_widget = QTableWidgetItem(table_title_name)
        table_title_widget.setFont(self.table_font)
        self.table_header.setItem(
            0, 0, table_title_widget
        )

        # Create a Create New 'button' by converting a cell to act like a button
        create_new_drill_profile_widget = QTableWidgetItem(
            "Create New")
        create_new_drill_profile_widget.setFont(self.table_font)
        self.table_header.setItem(
            0, 1, create_new_drill_profile_widget
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
        header_hor_head.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)
        self.table_header.setFixedHeight(
            int(self.table_header.sizeHint().height()/2))
        self.table_header.resizeRowsToContents()

    def get_drill_profiles_info(self):
        """Updates the backend with drill profile info
        """
        # Update drill profiles
        self.drill_profiles = self.profiler.get_profiles()
        # Update the length of the
        self.curr_drill_profiles_len = len(self.drill_profiles)

    def choose_main_table_click_action(self, item):
        # Unselect the currently picked cell
        self.main_table_view.selectedItems()[0].setSelected(False)

        # If a profile name has been clicked, then show a modal
        if item.column() == 0:
            self.drill_info_modal(item.row())
        # If the delete button has been clicked, go through the process of ensuring the user is fine with deleting it
        elif item.column() == 1:
            check_delete_modal_layout = QVBoxLayout()
            check_delete_modal_layout.addWidget(
                ProfileLabel("Are you sure you want to delete this drill profile?"))
            check_delete_modal = Modal(
                type="choice",
                layout=check_delete_modal_layout,
                window_title=self.main_table_view.item(item.row(), 0).text()
            )

            # If yes is clicked, delete the profile
            check_delete_modal.yes_button.clicked.connect(
                lambda: self.remove_drill_profile(item.row(), check_delete_modal))

            check_delete_modal.exec_()

    def remove_drill_profile(self, table_row, modal_object=None):
        """Removes a drill profile from the device

        Args:
            table_row (int): The table row number
            modal_object (QDialog): Instance of the modal view
        """

        # Fetch the location of the drill profile
        location = str(Path.home()) + '/Documents/ball_e_profiles/drill_profiles/' + \
            self.main_table_view.item(
                table_row, 0).text().replace(' ', '_').lower()
        # Remove the directory and remove the row from the table
        shutil.rmtree(location, ignore_errors=True)
        self.main_table_view.removeRow(table_row)

        # Update the drill profile instance
        self.get_drill_profiles_info()

        if modal_object is not None:
            # Close the modal
            modal_object.close()

    def create_new_drill_profile(self, drill_name):
        """Creates a drill profile locally in the device

        Args:
            drill_name(string): Drill Profile name
        """

        # Location where the profile will be stored
        location = str(Path.home()) + '/Documents/ball_e_profiles/drill_profiles/' + \
            drill_name.replace(' ', '_').lower()

        # Ensure that the drill profile does not exist (regardless of case-sensitivity). If it does, then throw an error informing the user about it
        try:
            # Create a directory and a .csv file containing the new drill profile
            pathlib.Path(location).mkdir(parents=True, exist_ok=False)
            pathlib.Path(location+'/{}.csv'.format(drill_name.replace(' ',
                                                                      '_').lower())).touch(exist_ok=False)
            # Append this new profile to the end of the table
            last_row_num = self.main_table_view.rowCount()
            self.main_table_view.insertRow(last_row_num)

            # Format the row accordingly with the drill profile name and a delete 'button'
            mod_drill_name_widget = QTableWidgetItem(drill_name.title())
            delete_row_widget = QTableWidgetItem('Delete')
            delete_row_widget.setBackground(
                QColor(sc.COLOR_ERROR)
            )
            delete_row_widget.setForeground(
                QColor(sc.COLOR_WHITE)
            )
            mod_drill_name_widget.setFont(self.table_font)
            delete_row_widget.setFont(self.table_font)
            mod_drill_name_widget.setTextAlignment(Qt.AlignLeft)
            delete_row_widget.setTextAlignment(Qt.AlignRight)

            # Set the contents in the table appropriately
            self.main_table_view.setItem(
                last_row_num, 0, mod_drill_name_widget)
            self.main_table_view.setItem(
                last_row_num, 1, delete_row_widget)

            self.main_table_view.resizeRowsToContents()
            # Update the drill profiles instance
            self.get_drill_profiles_info()

        # Let the user know that the profile exists using a modal
        except FileExistsError:
            error_modal_layout = QVBoxLayout()
            error_modal_layout.addWidget(ProfileLabel("Drill Exists"))
            Modal(
                type="error",
                layout=error_modal_layout,
                window_title=self.get_window_title()
            )

    def drill_info_modal(self, table_row):
        """Modal to show drill info

        Args:
            table_row (Object): The selected row in the table
        """

        # Get the drill's info
        drill_name = self.main_table_view.item(
            table_row, 0).text().replace(' ', '_').lower()
        drill_profile_path = self.drill_profiles[drill_name]

        modal_layout = QVBoxLayout()

        table_view = QTableWidget()
        table_view.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        drill_info = self.profiler.get_profile_info(drill_profile_path)

        # Otherwise, create and populate the table with drill information and times performed
        table_view.setRowCount(len(drill_info))
        table_view.setColumnCount(3)

        # Iterates through all the information and populates the table
        for curr_row, (ball_number, ball_specifics) in enumerate(zip(drill_info.keys(), drill_info.values())):
            ball_number_widget = QTableWidgetItem(ball_number)
            ball_target_location_widget = QTableWidgetItem(ball_specifics[0])
            ball_speed_widget = QTableWidgetItem(ball_specifics[1])
            self.table_font.setPixelSize(int(sc.FONT_L[:2]))
            ball_number_widget.setFont(self.table_font)
            ball_target_location_widget.setFont(self.table_font)
            ball_speed_widget.setFont(self.table_font)
            ball_number_widget.setTextAlignment(Qt.AlignCenter)
            ball_target_location_widget.setTextAlignment(Qt.AlignCenter)
            ball_speed_widget.setTextAlignment(Qt.AlignCenter)
            table_view.setItem(curr_row, 0, ball_number_widget)
            table_view.setItem(curr_row, 1, ball_target_location_widget)
            table_view.setItem(curr_row, 2, ball_speed_widget)
            drill_rof = ball_specifics[2]

        table_view.setHorizontalHeaderLabels(
            ["Ball #", "Location", "Speed"])
        table_view.verticalHeader().setVisible(False)
        table_view.resizeRowsToContents()

        table_view.horizontalHeader().setStyleSheet(
            """
            font-size: {font_size}
            """.format(font_size=sc.FONT_L)
        )

        table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        modal_layout.addWidget(ProfileLabel(
            "Drill Rate of Fire: {}".format(drill_rof)))
        modal_layout.addWidget(table_view)

        # Create a modal object to show all this information
        Modal(
            type="info",
            layout=modal_layout,
            window_title=drill_name.replace('_', ' ').title()
        )

    def create_new_drill_profile_modal_page_one(self, item):
        """The modal for creating a new drill profile

        Args:
            item (Object): The cell object selected in TableView
        """

        # Unselect the currently picked cell
        self.table_header.selectedItems()[0].setSelected(False)

        # Ensure that the user actually selected the Create New button
        if item.column() == 1:

            # Create a modal that will take user input for the drill name
            create_new_page_one = QDialog()

            create_new_page_one.setWindowFlags(Qt.WindowStaysOnTopHint |
                                               Qt.WindowCloseButtonHint)

            create_new_page_one.setWindowTitle("Create New Drill Profile")

            modal_page_one_layout = QVBoxLayout()

            modal_page_one_row_one_layout = QHBoxLayout()

            # Captures the name of the drill
            modal_page_one_row_one_layout.addWidget(
                ProfileLabel("Name: "))
            drill_name_input = LineEdit()
            modal_page_one_row_one_layout.addWidget(drill_name_input)
            modal_page_one_layout.addLayout(modal_page_one_row_one_layout)

            # Goes to the Next Page
            next_button = GenericButton("Next")
            modal_page_one_layout.addWidget(next_button)

            create_new_page_one.setLayout(modal_page_one_layout)

            next_button.clicked.connect(
                lambda: self.create_new_drill_profile_modal_page_two(create_new_page_one, drill_name_input.text(), after_name_input=True))

            create_new_page_one.exec_()

    def create_new_drill_profile_modal_page_two(self, modal, drill_name, after_name_input):

        if after_name_input:
            modal.close()
        else:
            modal.accept()

        # Create a modal that will take user input for the number of balls for the drill and the ROF
        create_new_page_two = QDialog()

        create_new_page_two.setWindowFlags(Qt.WindowStaysOnTopHint |
                                           Qt.WindowCloseButtonHint)

        create_new_page_two.setWindowTitle("Create New Drill Profile")

        create_new_page_two_layout = QVBoxLayout()

        create_new_page_two.setLayout(create_new_page_two_layout)

        # First, check that the drill profile can be validly created
        drill_location = str(Path.home()) + '/Documents/ball_e_profiles/drill_profiles/' + \
            drill_name.replace(' ', '_').lower()

        if after_name_input:
            if Path(drill_location).is_dir():
                error_modal_layout = QVBoxLayout()
                error_modal_layout.addWidget(ProfileLabel("Drill Exists"))
                Modal(
                    type="error",
                    layout=error_modal_layout,
                    window_title=self.get_window_title()
                )
                return
            else:
                self.create_new_drill_profile(drill_name)
                drill_location += '/{}.csv'.format(
                    drill_name.replace(' ', '_').lower())

        # Reset the current drill's balls and ROF to match with what will be shown on GUI
        # The minimum number of balls required to create any drills
        self.curr_drill_balls = 1

        # The minimum ROF for any drill
        self.curr_drill_rof = sc.MIN_ROF

        create_new_page_two_row_one_layout = QHBoxLayout()
        create_new_page_two_row_two_layout = QHBoxLayout()

        # Dropdown for the selection number of balls
        create_new_page_two_row_one_layout.addWidget(
            ProfileLabel("# of Balls: "))
        num_balls_input = Dropdown()
        for ball_count in range(sc.MAX_BALL_COUNT):
            num_balls_input.addItem(str(ball_count+1))
        num_balls_input.currentIndexChanged.connect(
            lambda: self.update_total_drill_balls(int(num_balls_input.currentText())))

        create_new_page_two_row_one_layout.addWidget(num_balls_input)
        # Dropdown for the Rate of Fire
        create_new_page_two_row_two_layout.addWidget(
            ProfileLabel("Rate of Fire (s/ball): "))
        rate_of_fire_input = Dropdown()
        for rate_of_fire in range(sc.MIN_ROF, sc.MAX_ROF+1):
            rate_of_fire_input.addItem(str(rate_of_fire))
        rate_of_fire_input.currentIndexChanged.connect(
            lambda: self.update_drill_rof(int(rate_of_fire_input.currentText())))
        create_new_page_two_row_two_layout.addWidget(rate_of_fire_input)
        create_new_page_two_layout.addLayout(
            create_new_page_two_row_one_layout)
        create_new_page_two_layout.addLayout(
            create_new_page_two_row_two_layout)

        # Goes to the Next Page
        next_button = GenericButton("Next")
        create_new_page_two_layout.addWidget(next_button)

        next_button.clicked.connect(
            lambda: self.create_new_drill_profile_modal_page_three(create_new_page_two, drill_name))

        exec_val = create_new_page_two.exec()

        if exec_val == QDialog.Rejected:
            self.remove_drill_profile(self.main_table_view.rowCount()-1)

    def create_new_drill_profile_modal_page_three(self, modal, drill_name):

        modal.accept()

        # Create a modal that will take user input for shot location and ball speed
        create_new_page_three = QDialog()

        create_new_page_three.setWindowFlags(Qt.WindowStaysOnTopHint |
                                             Qt.WindowCloseButtonHint)

        create_new_page_three.setWindowTitle("Create New Drill Profile")

        create_new_page_three_layout = QVBoxLayout()

        create_new_page_three.setLayout(create_new_page_three_layout)

        drill_location = str(Path.home()) + '/Documents/ball_e_profiles/drill_profiles/' + \
            drill_name.replace(' ', '_').lower(
        ) + '/{}.csv'.format(drill_name.replace(' ', '_').lower())

        modal_page_three_tab_widget = QTabWidget()

        with open(drill_location, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(
                ["Ball #", "Target Location", "Ball Speed", "Rate of Fire"]
            )
            for balls in range(self.curr_drill_balls):
                writer.writerow(["{}".format(
                    balls+1), "CM", "{}".format(sc.MIN_BALL_SPEED), "{}".format(self.curr_drill_rof)])
                modal_page_three_tab_widget.addTab(
                    DrillCreationWidget(drill_location, "{}".format(balls+1)), "Ball {}".format(balls+1))

        create_new_page_three_layout.addWidget(modal_page_three_tab_widget)

        back_button = GenericButton("Back")
        back_button.clicked.connect(
            lambda: self.create_new_drill_profile_modal_page_two(create_new_page_three, drill_name, after_name_input=False))
        create_new_page_three_layout.addWidget(back_button)

        save_button = GenericButton("Save")
        save_button.clicked.connect(
            lambda: create_new_page_three.accept())
        create_new_page_three_layout.addWidget(save_button)

        exec_val = create_new_page_three.exec()

        if exec_val == QDialog.Rejected:
            self.remove_drill_profile(self.main_table_view.rowCount()-1)

    def update_total_drill_balls(self, updated_drill_balls):
        self.curr_drill_balls = updated_drill_balls

    def update_drill_rof(self, updated_drill_rof):
        self.curr_drill_rof = updated_drill_rof

    def get_window_title(self):
        """Helper function to return this window's title

        Returns:
            [string]: This window's title
        """
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(DrillProfilesScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
