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
    from component_lineedit import LineEdit
    from component_modal import Modal
    from component_toolbar import ToolbarComponent
    from helper_profiler import Profiler
    from window_test import TestWindow

except ImportError:
    print("Imports failed")
finally:
    import shutil

    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QColor, QFont
    from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QHeaderView,
                                 QSizePolicy, QTableWidget, QTableWidgetItem,
                                 QVBoxLayout, QWidget)


class GoalieProfilesScreen(QWidget):
    """Screen to create, delete, and view Goalie Profiles

    Args:
        QWidget ([PyQt5 Widget]): This object will be used by the Main Window to show on screen
    """

    def __init__(self):
        """Widget Initialization
        """
        super().__init__()

        self.window_title = "Goalie Profiles"

        # Get the goalie profiles available on the device
        self.profiler = Profiler('goalie_profiles')
        self.get_goalie_profiles_info()

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
            table_title_name="Goalie Profiles",
            header_clicked_action=self.create_new_goalie_profile_modal)
        self.screen_layout.addWidget(self.table_header)

        # Create the main table and add to the layout
        self.create_main_table_view(profile_dict_obj=self.goalie_profiles,
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

        # Create the table object that acts as the "header" for the main goalie profile table view
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
        create_new_goalie_profile_widget = QTableWidgetItem(
            "Create New")
        create_new_goalie_profile_widget.setFont(self.table_font)
        self.table_header.setItem(
            0, 1, create_new_goalie_profile_widget
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
        self.table_header.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Fixed
        )
        self.table_header.setFixedHeight(
            int(self.table_header.sizeHint().height()/2))
        self.table_header.resizeRowsToContents()

    def get_goalie_profiles_info(self):
        """Updates the backend with goalie profile info
        """
        # Update goalie profiles
        self.goalie_profiles = self.profiler.get_profiles()
        # Update the length of the
        self.curr_goalie_profiles_len = len(self.goalie_profiles)

    def choose_main_table_click_action(self, item):
        # Unselect the currently picked cell
        self.main_table_view.selectedItems()[0].setSelected(False)

        # If a profile name has been clicked, then show a modal
        if item.column() == 0:
            self.goalie_info_modal(item.row())
        # If the delete button has been clicked, go through the process of ensuring the user is fine with deleting it
        elif item.column() == 1:

            check_delete_modal_layout = QVBoxLayout()
            check_delete_modal_layout.addWidget(
                ProfileLabel("Are you sure you want to delete this goalie profile?"))
            check_delete_modal = Modal(
                type="choice",
                layout=check_delete_modal_layout,
                window_title=self.main_table_view.item(item.row(), 0).text()
            )

            # If yes is clicked, delete the profile
            check_delete_modal.yes_button.clicked.connect(
                lambda: self.remove_goalie_profile(item.row(), check_delete_modal))

            check_delete_modal.exec_()

    def remove_goalie_profile(self, table_row, modal_object):
        """Removes a goalie profile from the device

        Args:
            table_row (int): The table row number
            modal_object (QDialog): Instance of the modal view
        """

        # Fetch the location of the goalie profile
        location = str(Path.home()) + '/Documents/ball_e_profiles/goalie_profiles/' + \
            self.main_table_view.item(
                table_row, 0).text().replace(' ', '_').lower()
        # Remove the directory and remove the row from the table
        shutil.rmtree(location, ignore_errors=True)
        self.main_table_view.removeRow(table_row)

        # Update the goalie profile instance
        self.get_goalie_profiles_info()

        # Close the modal
        modal_object.close()

    def create_new_goalie_profile_modal(self, item):
        """The modal for creating a new goalie profile

        Args:
            item (Object): The cell object selected in TableView
        """
        # Unselect the currently picked cell
        self.table_header.selectedItems()[0].setSelected(False)

        # Ensure that the user actually selected the Create New button
        if item.column() == 1:

            # Create a modal that will take user input for the goalie name

            create_goalie_profile_modal_layout = QHBoxLayout()
            create_goalie_profile_modal_layout.addWidget(
                ProfileLabel("Name: "))
            goalie_name_input = LineEdit()
            create_goalie_profile_modal_layout.addWidget(goalie_name_input)
            new_goalie_profile_save_button = GenericButton("Save")
            new_goalie_profile_save_button.clicked.connect(
                lambda: self.create_new_goalie_profile(goalie_name_input.text()))
            create_goalie_profile_modal_layout.addWidget(
                new_goalie_profile_save_button)

            modal_title = "Create New Goalie Profile"
            Modal(
                type="info",
                layout=create_goalie_profile_modal_layout,
                window_title=modal_title
            )

    def create_new_goalie_profile(self, goalie_name):
        """Creates a goalie profile locally in the device

        Args:
            goalie_name (string): Goalie Profile name
        """

        # Location where the profile will be stored
        location = str(Path.home()) + '/Documents/ball_e_profiles/goalie_profiles/' + \
            goalie_name.replace(' ', '_').lower()

        # Ensure that the goalie profile does not exist (regardless of case-sensitivity). If it does, then throw an error informing the user about it
        try:
            # Create a directory and a .csv file containing the new goalie profile
            pathlib.Path(location).mkdir(parents=True, exist_ok=False)
            pathlib.Path(location+'/{}.csv'.format(goalie_name.replace(' ',
                                                                       '_').lower())).touch(exist_ok=False)
            # Append this new profile to the end of the table
            last_row_num = self.main_table_view.rowCount()
            self.main_table_view.insertRow(last_row_num)

            # Format the row accordingly with the goalie profile name and a delete 'button'
            mod_goalie_name_widget = QTableWidgetItem(goalie_name)
            delete_row_widget = QTableWidgetItem('Delete')
            delete_row_widget.setBackground(
                QColor(sc.COLOR_ERROR)
            )
            delete_row_widget.setForeground(
                QColor(sc.COLOR_WHITE)
            )
            mod_goalie_name_widget.setFont(self.table_font)
            delete_row_widget.setFont(self.table_font)
            mod_goalie_name_widget.setTextAlignment(Qt.AlignLeft)
            delete_row_widget.setTextAlignment(Qt.AlignRight)

            # Set the contents in the table appropriately
            self.main_table_view.setItem(
                last_row_num, 0, mod_goalie_name_widget)
            self.main_table_view.setItem(
                last_row_num, 1, delete_row_widget)

            self.main_table_view.resizeRowsToContents()
            # Update the goalie profiles instance
            self.get_goalie_profiles_info()

        # Let the user know that the profile exists using a modal
        except FileExistsError:
            error_modal_layout = QVBoxLayout()
            error_modal_layout.addWidget(ProfileLabel("Goalie Exists"))
            Modal(
                type="error",
                layout=error_modal_layout,
                window_title=self.get_window_title()
            )

    def goalie_info_modal(self, table_row):
        """Modal to show Goalie info

        Args:
            table_row (Object): The selected row in the table
        """

        # If the selected row was newly created, then just display the modal saying "No information yet and quit"
        if table_row >= self.curr_goalie_profiles_len:
            info_modal_layout = QVBoxLayout()
            info_modal_layout.addWidget(ProfileLabel("No information yet."))
            Modal(
                type="info",
                layout=info_modal_layout,
                window_title=self.main_table_view.item(table_row, 0).text()
            )
            return

        # Get the goalie's info
        goalie_name = self.main_table_view.item(
            table_row, 0).text().replace(' ', '_').lower()
        goalie_profile_path = self.goalie_profiles[goalie_name]

        modal_layout = QVBoxLayout()

        table_view = QTableWidget()
        table_view.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        goalie_info = self.profiler.get_profile_info(goalie_profile_path)

        # If no info has been populated, also show that "No information yet" and quit
        if(len(goalie_info) == 0):
            info_modal_layout = QVBoxLayout()
            info_modal_layout.addWidget(ProfileLabel("No information yet."))
            Modal(
                type="info",
                layout=info_modal_layout,
                window_title=goalie_name.replace('_', ' ').title()
            )
            return

        # Otherwise, create and populate the table with drill information and times performed
        table_view.setRowCount(len(goalie_info))
        table_view.setColumnCount(2)

        # Iterates through all the information and populates the table
        for curr_row, (drill_info, date_info) in enumerate(zip(goalie_info.keys(), goalie_info.values())):
            drill_name_widget = QTableWidgetItem(drill_info)
            date_info_widget = QTableWidgetItem(date_info)
            self.table_font.setPixelSize(int(sc.FONT_L[:2]))
            drill_name_widget.setFont(self.table_font)
            date_info_widget.setFont(self.table_font)
            drill_name_widget.setTextAlignment(Qt.AlignCenter)
            date_info_widget.setTextAlignment(Qt.AlignCenter)
            table_view.setItem(curr_row, 0, drill_name_widget)
            table_view.setItem(curr_row, 1, date_info_widget)

        table_view.setHorizontalHeaderLabels(
            ["Drill History", "Date"])
        table_view.verticalHeader().setVisible(False)
        table_view.resizeRowsToContents()

        table_view.horizontalHeader().setStyleSheet(
            """
            font-size: {font_size}
            """.format(font_size=sc.FONT_L)
        )

        table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        modal_layout.addWidget(table_view)

        # Create a modal object to show all this information
        Modal(
            type="info",
            layout=modal_layout,
            window_title=goalie_name.replace('_', ' ').title()
        )

    def get_window_title(self):
        """Helper function to return this window's title

        Returns:
            [string]: This window's title
        """
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(GoalieProfilesScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
