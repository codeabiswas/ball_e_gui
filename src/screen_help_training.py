import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QListWidget, QListWidgetItem,
                             QMessageBox, QVBoxLayout, QWidget)

import helper_doc_reader as hdr
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class TrainingHelpScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Help: Training"

        # Get the docs for this section
        doc_reader = hdr.DocReader('training/training_doc.md')
        self.docs = doc_reader.get_doc()

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title, "Back to Help")

        screen_layout.addWidget(self.toolbar)

        self.scroll = QListWidget()

        for i in self.docs.keys():
            self.scroll.addItem(QListWidgetItem(i))

        self.scroll.itemSelectionChanged.connect(self.pop_up_generator)

        screen_layout.addWidget(self.scroll)

        self.setLayout(screen_layout)

    def pop_up_generator(self):
        selected_data = self.scroll.selectedIndexes()[0]

        pop_up = QMessageBox()
        pop_up.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        pop_up.setWindowTitle(self.window_title)
        pop_up.setStandardButtons(QMessageBox.Close)
        pop_up.setText(selected_data.data())
        pop_up.setInformativeText(self.docs[selected_data.data()])

        pop_up.setStyleSheet(
            """
            font-size: 22px;
            """
        )

        pop_up.exec_()

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(TrainingHelpScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
