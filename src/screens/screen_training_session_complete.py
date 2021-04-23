try:
    import pathlib
    import sys
    sys.path.append(
        "{}/Developer/ball_e_gui/src/components".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/helpers".format(pathlib.Path.home()))
    sys.path.append(
        "{}/Developer/ball_e_gui/src/windows".format(pathlib.Path.home()))

    from component_labels import ProfileLabel
    from component_toolbar import ToolbarComponent
    from window_test import TestWindow
except ImportError:
    print("Imports failed")
finally:

    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget


class TrainingSessionCompleteScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Training Complete"

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title)

        screen_layout.addWidget(self.toolbar)

        screen_layout.addWidget(ProfileLabel(
            "Training Complete"))

        self.setLayout(screen_layout)

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingSessionCompleteScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
