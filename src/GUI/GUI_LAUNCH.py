"""
@Author:    chenghua.Wang
@file:      src/GUI/main_ui.py
@brief:     A GUI Launch enter.   
"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

import API.StyleModel as StyleModel
import GUI.API.main_window as main_window
import GUI.API.StyleModel as StyleModel
import logic.SqlSearch as SqlSearch

from core.SqlMan import SqlMan
from core.Phaser import PhaserLoginCfg

class RUN:
    def __init__(self):
        self.LoginCfg = PhaserLoginCfg()
        self.SqlConn = SqlMan(self.LoginCfg.GetUser(0))

    def __call__(self, *args, **kwds):
        # High DPI support
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        # Qt Main app
        app = QApplication(sys.argv)
        StyleModel.style_modeling(app, 'dark_blue.xml')
        ui = main_window.UI_MainWindow(QMainWindow())
        sys.exit(app.exec_())

if __name__ == '__main__':
    RUN()()