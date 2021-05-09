"""
component_drill_creation_widget.py
---
This file contains the MainWindow class. It is the frameless window which controls and displays all the screens (i.e.: QWidget Objects) in Ball-E's user interface.
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

    import style_constants as sc
    from helper_profiler import Profiler

    from component_dropdown import Dropdown
    from component_labels import ProfileLabel
except ImportError:
    print("{}: Imports failed".format(__file__))
finally:
    import csv

    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter, QPen, QPixmap
    from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class DrillCreationWidget(QWidget):
    """DrillCreationWidget.

    This class configures and creates all required components and logic to create drills.
    """

    def __init__(self, local_location, ball_number):
        """__init__.

        Initializes the Drill Creation Widget with the path where this profiles needs to be saved and how many balls the drill consists of.
        :param local_location: String of the path where this drill would be saved
        :param ball_number: Integer number of balls required for this drill
        """
        super().__init__()

        self.local_location = local_location
        self.ball_number = ball_number

        self.drill_profiler = Profiler("drill_profiles")

        widget_layout = QVBoxLayout()

        # Initialize where all the balls will be placed and their speed by default (Center Middle location @ 30 MPH)
        self.shot_location_label = ProfileLabel("Shot Location: Center Middle")
        self.lax_goal_label = QLabel()
        lax_goal_img_location = str(
            pathlib.Path.home()) + '/Developer/ball_e_gui/src/images/lax_goal.png'
        pixmap_object = QPixmap()
        pixmap_object.load(lax_goal_img_location)
        self.scaled_pixmap_obj = pixmap_object.scaled(pixmap_object.width()-300,
                                                      pixmap_object.height()-300)
        # What function to call when the Lacrosse goal picture has been clicked
        self.lax_goal_label.mousePressEvent = self.save_shot_location

        # Draw the lines on the Lax goal image. These lines divide the goal into 9 sections.
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

        # Update the image with the lines drawn
        self.lax_goal_label.setPixmap(self.scaled_pixmap_obj)

        # Create dropdown for selecting the speed
        speed_selection_label = ProfileLabel("Ball Speed (in MPH)")
        speed_selection_dropdown = Dropdown()
        for ball_count in range(sc.MIN_BALL_SPEED, sc.MAX_BALL_SPEED+1, 5):
            speed_selection_dropdown.addItem(str(ball_count))
        speed_selection_dropdown.currentIndexChanged.connect(
            lambda: self.save_speed_selection(speed_selection_dropdown.currentText()))

        # Add al the widgets
        widget_layout.addWidget(self.shot_location_label)
        widget_layout.addWidget(self.lax_goal_label)
        widget_layout.addWidget(speed_selection_label)
        widget_layout.addWidget(speed_selection_dropdown)

        self.setLayout(widget_layout)

    def save_shot_location(self, event):
        """save_shot_location.

        This function processes and saves the location for the ball that the user clicked on.

        :param event: Object which contains the coordinates where the user clicked
        """

        # Get the X and Y coordinates
        x_coord = event.pos().x()
        y_coord = event.pos().y()

        # The following code figures out exactly which of the 9 sections the user clicked on
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

        drill_info = self.drill_profiler.get_profile_info(self.local_location)

        # Figure out which of the 9 locations the user has clicked on and save it to each ball
        if top_flag and left_flag:
            self.shot_location_label.setText(
                "Shot Location: Top Left")
            drill_info[self.ball_number][0] = "TL"
        elif top_flag and right_flag:
            self.shot_location_label.setText(
                "Shot Location: Top Right")
            drill_info[self.ball_number][0] = "TR"
        elif top_flag and middle_flag:
            self.shot_location_label.setText(
                "Shot Location: Top Middle")
            drill_info[self.ball_number][0] = "TM"
        elif center_flag and left_flag:
            self.shot_location_label.setText(
                "Shot Location: Center Left")
            drill_info[self.ball_number][0] = "CL"
        elif center_flag and right_flag:
            self.shot_location_label.setText(
                "Shot Location: Center Right")
            drill_info[self.ball_number][0] = "CR"
        elif center_flag and middle_flag:
            self.shot_location_label.setText(
                "Shot Location: Center Middle")
            drill_info[self.ball_number][0] = "CM"
        elif bottom_flag and left_flag:
            self.shot_location_label.setText(
                "Shot Location: Bottom Left")
            drill_info[self.ball_number][0] = "BL"
        elif bottom_flag and right_flag:
            self.shot_location_label.setText(
                "Shot Location: Bottom Right")
            drill_info[self.ball_number][0] = "BR"
        elif bottom_flag and middle_flag:
            self.shot_location_label.setText(
                "Shot Location: Bottom Middle")
            drill_info[self.ball_number][0] = "BM"

        # Update the information
        self.update_drill_local_file(drill_info)

    def save_speed_selection(self, selected_speed):
        """save_speed_selection.

        This function saves the ball's set speed

        :param selected_speed: Integer number of a value in MPH for what the ball speed should be
        """

        drill_info = self.drill_profiler.get_profile_info(self.local_location)
        drill_info[self.ball_number][1] = selected_speed

        self.update_drill_local_file(drill_info)

    def update_drill_local_file(self, drill_info):
        """update_drill_local_file.

        Updates the updated drill information to the appropriate .csv file

        :param drill_info: Dictionary which consists of the drill's information
        """
        with open(self.local_location, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(
                ["Ball #", "Target Location", "Ball Speed", "Rate of Fire"]
            )
            for ball in drill_info:
                writer.writerow([str(ball), drill_info[ball][0],
                                 drill_info[ball][1], drill_info[ball][2]])
