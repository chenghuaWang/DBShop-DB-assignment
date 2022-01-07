# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Insert_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1458, 1004)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.AddItemButton = QtWidgets.QPushButton(Form)
        self.AddItemButton.setObjectName("AddItemButton")
        self.verticalLayout.addWidget(self.AddItemButton)
        self.SubmitButton = QtWidgets.QPushButton(Form)
        self.SubmitButton.setObjectName("SubmitButton")
        self.verticalLayout.addWidget(self.SubmitButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.AddItemButton.setText(_translate("Form", "PushButton"))
        self.SubmitButton.setText(_translate("Form", "PushButton"))

