"""
@Author:    chenghua.Wang
@file:      src/GUI/API/Inert_window.py
@brief:     search Table window for MainWindow class.
"""
import os
import sys

sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QDialog, QApplication, QWidget, qApp, QInputDialog
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor

class SearchTable_Window(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(974, 712)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Search Concequence window"))

    def UpdateTableData(self, func_cls, data, describe):
        func_cls.TableViewUpdate(self, describe, data)

    def show(self) -> None:
        return super().show()

