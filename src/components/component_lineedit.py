try:
    import pathlib
    import sys
    sys.path.append(
        "{}/Developer/ball_e_gui/src/helpers".format(pathlib.Path.home()))

    import style_constants as sc
except ImportError:
    print("Imports failed")
finally:
    from PyQt5.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

        self.line_edit_font = self.font()
        self.line_edit_font.setPointSize(int(sc.FONT_XL[0:2]))
        self.setFont(self.line_edit_font)
