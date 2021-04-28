try:
    import pathlib
    import sys
    sys.path.append(
        "{}/Developer/ball_e_gui/src/components".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/windows".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_image_processing/src".format(pathlib.Path.home()))

    from component_button import GenericButton
    from component_labels import ProfileLabel
    from component_toolbar import ToolbarComponent
    from goal_distance_calculator import GoalDistanceCalculator
    from window_test import TestWindow

except ImportError:
    print("{}: Imports failed".format(__file__))
finally:

    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap
    from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel,
                                 QVBoxLayout, QWidget)


class TrainingGoalCalibrationScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Goal Calibration"

        self.click_counter = 0

        # This object will keep track of what the distance of Ball-E from the goal is
        self.goal_distance = None

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(
            self.window_title, "Back to Goal Calib. \nSetup")

        screen_layout.addWidget(self.toolbar)

        self.info_label = ProfileLabel(
            "Please select the 4 corners of the goal, going clockwise from the top-left corner")
        screen_layout.addWidget(self.info_label)

        self.lax_goal_label = QLabel()
        screen_layout.addWidget(self.lax_goal_label)
        # NOTE: This will change to temp_training_lax_goal.png
        self.lax_goal_img_location = str(
            # Path.home()) + '/Developer/ball_e_gui/src/images/lax_goal.png'
            pathlib.Path.home()) + '/Developer/ball_e_gui/src/images/temp_training_lax_goal.png'

        self.pixmap_object = QPixmap()
        self.pixmap_object.load(self.lax_goal_img_location)
        self.lax_goal_label.mousePressEvent = self.draw_user_input
        self.lax_goal_label.setPixmap(self.pixmap_object)

        self.button_layout = QHBoxLayout()
        self.reset_button = GenericButton("Reset")
        self.reset_button.clicked.connect(self.reset_lines)
        self.reset_button.setVisible(False)
        self.next_page_button = GenericButton("Next")
        self.next_page_button.setVisible(False)

        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.next_page_button)

        screen_layout.addLayout(self.button_layout)

        self.top_left_coord = None
        self.top_right_coord = None
        self.bottom_right_coord = None
        self.bottom_left_coord = None

        self.setLayout(screen_layout)

    def update_lax_goal_pic(self):
        self.pixmap_object = QPixmap()
        self.pixmap_object.load(self.lax_goal_img_location)
        self.lax_goal_label.mousePressEvent = self.draw_user_input
        self.lax_goal_label.setPixmap(self.pixmap_object)

    def reset_lines(self):
        # Reset click counter
        self.click_counter = 0

        # Clear the image
        # NOTE: This will change to temp_training_lax_goal.png
        self.lax_goal_img_location = str(
            pathlib.Path.home()) + '/Developer/ball_e_gui/src/images/temp_training_lax_goal.png'

        self.pixmap_object = QPixmap()
        self.pixmap_object.load(self.lax_goal_img_location)
        self.lax_goal_label.mousePressEvent = self.draw_user_input
        self.lax_goal_label.setPixmap(self.pixmap_object)

        self.reset_button.setVisible(False)
        self.next_page_button.setVisible(False)

        self.info_label.setText(
            "Please select the 4 corners of the goal, going clockwise from the top-left corner")

    def draw_user_input(self, event):
        x_coord = event.pos().x()
        y_coord = event.pos().y()

        if self.click_counter < 4:
            self.click_counter += 1

            painter_obj = QPainter(self.pixmap_object)
            painter_obj.setPen(QPen(Qt.green, 12, Qt.SolidLine))
            painter_obj.setBrush(QBrush(Qt.green, Qt.SolidPattern))

            painter_obj.drawEllipse(event.pos(), 20, 20)

            painter_obj.end()

            self.lax_goal_label.setPixmap(self.pixmap_object)

            if self.click_counter == 1:
                self.top_left_coord = (x_coord, y_coord)

            elif self.click_counter == 2:
                self.top_right_coord = (x_coord, y_coord)

            elif self.click_counter == 3:
                self.bottom_right_coord = (x_coord, y_coord)

            elif self.click_counter == 4:
                self.bottom_left_coord = (x_coord, y_coord)
                self.reset_button.setVisible(True)
                self.next_page_button.setVisible(True)
                self.draw_lines()

                # Accumulate all the points acquired from the user in a list
                points_drawn = [self.top_left_coord, self.top_right_coord,
                                self.bottom_right_coord, self.bottom_left_coord]
                # Create distance from goal calculator object
                goal_distance_calculator = GoalDistanceCalculator(points_drawn)
                # Get the distance calculated in ft.
                self.goal_distance = goal_distance_calculator.get_obj_distance()/12

                self.info_label.setText(
                    "Distance Calculated: {%.2f} ft.\nThese will be your bounds. If you would like to redo this, click on the Reset button".format(goal_distance))

    def draw_lines(self):

        painter_obj = QPainter(self.pixmap_object)
        painter_obj.setPen(QPen(Qt.green, 12, Qt.SolidLine))

        # Draw the perimeter
        painter_obj.drawLine(
            self.top_left_coord[0], self.top_left_coord[1], self.top_right_coord[0], self.top_right_coord[1])

        painter_obj.drawLine(
            self.top_left_coord[0], self.top_left_coord[1], self.bottom_left_coord[0], self.bottom_left_coord[1])

        painter_obj.drawLine(
            self.top_right_coord[0], self.top_right_coord[1], self.bottom_right_coord[0], self.bottom_right_coord[1])

        painter_obj.drawLine(
            self.bottom_left_coord[0], self.bottom_left_coord[1], self.bottom_right_coord[0], self.bottom_right_coord[1])

        # Calculate Left and Right coordinates for the latitudes
        top_one_third_coord_left = (int((2/3)*(self.top_left_coord[0]))+int((1/3)*(self.bottom_left_coord[0])), int(
            (2/3)*(self.top_left_coord[1]))+int((1/3)*(self.bottom_left_coord[1])))
        top_two_third_coord_left = (int((1/3)*(self.top_left_coord[0]))+int((2/3)*(self.bottom_left_coord[0])), int(
            (1/3)*(self.top_left_coord[1]))+int((2/3)*(self.bottom_left_coord[1])))

        top_one_third_coord_right = (int((2/3)*(self.top_right_coord[0]))+int((1/3)*(self.bottom_right_coord[0])), int(
            (2/3)*(self.top_right_coord[1]))+int((1/3)*(self.bottom_right_coord[1])))
        top_two_third_coord_right = (int((1/3)*(self.top_right_coord[0]))+int((2/3)*(self.bottom_right_coord[0])), int(
            (1/3)*(self.top_right_coord[1]))+int((2/3)*(self.bottom_right_coord[1])))

        # Draw latitudes
        painter_obj.drawLine(top_one_third_coord_left[0], top_one_third_coord_left[1],
                             top_one_third_coord_right[0], top_one_third_coord_right[1])
        painter_obj.drawLine(top_two_third_coord_left[0], top_two_third_coord_left[1],
                             top_two_third_coord_right[0], top_two_third_coord_right[1])

        # Calculate Top and Bottom coordinates for the longitudes
        left_one_third_coord_top = (int((2/3)*(self.top_left_coord[0]))+int((1/3)*(self.top_right_coord[0])), int(
            (2/3)*(self.top_left_coord[1]))+int((1/3)*(self.top_right_coord[1])))
        left_two_third_coord_top = (int((1/3)*(self.top_left_coord[0]))+int((2/3)*(self.top_right_coord[0])), int(
            (1/3)*(self.top_left_coord[1]))+int((2/3)*(self.top_right_coord[1])))

        left_one_third_coord_bottom = (int((2/3)*(self.bottom_left_coord[0]))+int((1/3)*(self.bottom_right_coord[0])), int(
            (2/3)*(self.bottom_left_coord[1]))+int((1/3)*(self.bottom_right_coord[1])))
        left_two_third_coord_bottom = (int((1/3)*(self.bottom_left_coord[0]))+int((2/3)*(self.bottom_right_coord[0])), int(
            (1/3)*(self.bottom_left_coord[1]))+int((2/3)*(self.bottom_right_coord[1])))

        # Draw longitudes
        painter_obj.drawLine(left_one_third_coord_top[0], left_one_third_coord_top[1],
                             left_one_third_coord_bottom[0], left_one_third_coord_bottom[1])
        painter_obj.drawLine(left_two_third_coord_top[0], left_two_third_coord_top[1],
                             left_two_third_coord_bottom[0], left_two_third_coord_bottom[1])

        painter_obj.end()

        self.lax_goal_label.setPixmap(self.pixmap_object)

    def get_goal_distance(self):
        return self.goal_distance/12

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingGoalCalibrationScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
