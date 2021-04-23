try:
    import pathlib
    import sys
    sys.path.append(
        "{}/Developer/ball_e_gui/src/components".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/helpers".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/windows".format(pathlib.Path.home()))

    from component_button import FullPageButton
    from component_toolbar import ToolbarComponent
    from window_test import TestWindow
except ImportError:
    print("Imports failed")
finally:
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget


class HelpScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Help"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        self.calibration_screen_button = FullPageButton("Calibration")
        self.training_screen_button = FullPageButton("Training")
        self.profiles_screen_button = FullPageButton("Profiles")
        self.session_recording_screen_button = FullPageButton(
            "Session Recording")

        screen_layout.addWidget(self.calibration_screen_button)
        screen_layout.addWidget(self.training_screen_button)
        screen_layout.addWidget(self.profiles_screen_button)
        screen_layout.addWidget(self.session_recording_screen_button)

        self.setLayout(screen_layout)

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(HelpScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
