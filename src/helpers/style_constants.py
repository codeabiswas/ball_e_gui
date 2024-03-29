"""
style_constants.py
---
This file contains mainly style constants that are used throughout the GUI to maintain coherence across the design style of Ball-E's app.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget

FONT_S = "16px"
FONT_M = "22px"
FONT_L = "40px"
FONT_XL = "50px"
FONT_XXL = "80px"

COLOR_TOOLBAR = "#2E75B6"
COLOR_INFO = "#C55A11"
COLOR_ERROR = "#C00000"
COLOR_WHITE = "#FFFFFF"

MIN_BALL_COUNT = 1
MAX_BALL_COUNT = 36
MIN_ROF = 5
MAX_ROF = 25
MIN_BALL_SPEED = 30
MAX_BALL_SPEED = 100
# In Yards
MIN_DISTANCE = 5
MAX_DISTANCE = 20

# Table Header Height 22+8=30px
TABLE_HEADER_HEIGHT = 30

app = QApplication(sys.argv)
SCREEN_HEIGHT = QDesktopWidget().screenGeometry(0).height()
SCREEN_WIDTH = QDesktopWidget().screenGeometry(0).width()
# Preventing Segmentation Fault
app = None
