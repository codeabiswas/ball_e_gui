import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QListWidget, QListWidgetItem,
                             QMessageBox, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

import helper_doc_reader as hdr
from component_labels import ProfileLabel
from component_modal import Modal
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class ListItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        font = QFont()
        font.setPixelSize(22)
        self.setFont(font)


class SessionRecordingHelpScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.window_title = "Help: Session Recording"

        # Get the docs for this section
        doc_reader = hdr.DocReader(
            'session_recording/session_recording_doc.md')
        self.docs = doc_reader.get_doc()

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(self.window_title, "Back to Help")

        screen_layout.addWidget(self.toolbar)

        self.scroll = QListWidget()

        for i in self.docs.keys():
            self.scroll.addItem(ListItem(i))

        self.scroll.itemSelectionChanged.connect(self.pop_up_generator)

        screen_layout.addWidget(self.scroll)

        self.setLayout(screen_layout)

    def pop_up_generator(self):
        selected_data = self.scroll.selectedIndexes()[0]

        modal_info_layout = QVBoxLayout()

        answer_label = ProfileLabel(self.docs[selected_data.data()])
        answer_label.setWordWrap(True)
        modal_info_layout.addWidget(answer_label)

        Modal(
            type="info",
            layout=modal_info_layout,
            window_title=selected_data.data()
        )

    def get_window_title(self):
        return self.window_title


def main():
    app = QApplication(sys.argv)
    win = TestWindow(SessionRecordingHelpScreen())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
