"""
@Author:    chenghua.Wang
@file:      src/GUI/API/select_window.py
@brief:     select_window called from main window.
"""
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from core.SqlMan import SqlSearch_DS

class Select_Window(QtWidgets.QDialog):
    def __init__(self, MainWindow, func_class):
        super().__init__()
        self.MainWindow = MainWindow
        self.func_class = func_class
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(300, 192)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setEnabled(True)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        # -- Add action
        self.pushButton.clicked.connect(self.actionBottonSelect)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Select"))

    def updateSelectBar(self, describe):
        self.comboBox.clear()
        self.comboBox.addItems(describe)

    def actionBottonSelect(self):
        CurrentText = self.comboBox.currentText()
        WhereText = self.lineEdit.text()
        self.lineEdit.setText("")
        _new_describe_ = self.MainWindow.TableStatus.describe
        LOC = """
_new_data_ = []
for item in self.MainWindow.TableStatus.data.m_row:
    if item[_new_describe_.index({a})] {b}:
        _new_data_.append(item)
self.MainWindow.SearchTable_childWindow.UpdateTableData(self.func_class, SqlSearch_DS(_new_data_), _new_describe_)
self.MainWindow.SearchTable_childWindow.show()
        """.format(
            a=("\""+CurrentText+"\""),
            b=WhereText,
        )
        exec(LOC)
        self.close()

    def show(self) -> None:
        return super().show()
