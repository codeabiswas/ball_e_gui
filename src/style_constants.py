import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget

FONT_S = "16px"
FONT_M = "22px"
FONT_L = "40px"
FONT_XL = "50px"
FONT_XXL = "60px"

COLOR_TOOLBAR = "#2E75B6"
COLOR_INFO = "#C55A11"
COLOR_ERROR = "#C00000"
COLOR_WHITE = "#FFFFFF"

# Table Header Height 22+8=30px
TABLE_HEADER_HEIGHT = 30

app = QApplication(sys.argv)
SCREEN_HEIGHT = QDesktopWidget().screenGeometry(0).height()
SCREEN_WIDTH = QDesktopWidget().screenGeometry(0).width()
# Preventing Segmentation Fault
app = None
