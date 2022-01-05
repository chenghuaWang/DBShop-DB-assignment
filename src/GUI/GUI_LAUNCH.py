"""
@Author:    chenghua.Wang
@file:      src/GUI/main_ui.py
@brief:     A GUI Launch enter.   
"""

import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

import GUI.API.main_window as main_window
import GUI.API.StyleModel as StyleModel

def LAUNCH_MAIN_GUI():
    app = QApplication(sys.argv)
    StyleModel.style_modeling(app, 'dark_lightgreen.xml')
    ex = main_window.MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    LAUNCH_MAIN_GUI()