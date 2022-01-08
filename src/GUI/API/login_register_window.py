import os
import sys
import hashlib

from PyQt5 import QtCore, QtGui, QtWidgets
from logic.SqlInsert import SqlInsert

class Login_Register_Window(QtWidgets.QDialog):
    def __init__(self, MainWindow, func_class, login_main_logic):
        super().__init__()
        self.MainWindow = MainWindow
        self.func_class = func_class
        self.login_main_logic = login_main_logic
        self.mode = " "
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(385, 261)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 4, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        # -- LineEdit Custom
        self.lineEdit.setPlaceholderText("ID")
        self.lineEdit_2.setPlaceholderText("Password")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        # -- end of LineEdit Custom
        # -- buttom action
        self.pushButton.clicked.connect(lambda: self.actionButtonCancel())
        self.pushButton_2.clicked.connect(lambda: self.actionButtonSubmit())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "账户"))
        self.label_2.setText(_translate("Form", "密码"))
        self.pushButton.setText(_translate("Form", "取消"))
        self.pushButton_2.setText(_translate("Form", "提交"))

    def actionButtonSubmit(self):
        self.MainWindow.id_pwd[2] = self.MainWindow.id_pwd[3] = False
        if self.mode == "Login":
            id = self.lineEdit.text()
            pwd = self.lineEdit_2.text()
            self.MainWindow.id_pwd[0] = id
            self.MainWindow.id_pwd[2] = True
            self.MainWindow.id_pwd[1] = pwd
            self.MainWindow.id_pwd[3] = True
            self.MainWindow.UserStatus.Update(id[0], id)
            self.login_main_logic.main(self.MainWindow, id[0], id, pwd)
        elif self.mode == "Register":
            id = self.lineEdit.text()
            pwd = self.lineEdit_2.text()
            pwd = hashlib.md5(pwd.encode("utf8")).hexdigest()
            if id[0] == "C":
                SQL_sentence = "insert into C values('{a}','{b}','{c}','{d}');".format(
                    a=id,
                    b='Default',
                    c='11111111111',
                    d='Default'
                )
                SqlInsert.EX_I(self.MainWindow.SqlConn, SQL_sentence)
                SQL_sentence = "insert into CM values('{a}','{b}')".format(
                    a=id,
                    b=pwd
                )
                SqlInsert.EX_I(self.MainWindow.SqlConn, SQL_sentence)
            elif id[0] == "P":
                SQL_sentence = "insert into GG(GGNo, GGName, GGAddr) values('{a}','{b}','{c}');".format(
                    a=id,
                    b='Default',
                    c='Default'
                )
                SqlInsert.EX_I(self.MainWindow.SqlConn, SQL_sentence)
                SQL_sentence = "insert into GGM values('{a}','{b}')".format(
                    a=id,
                    b=pwd
                )
                SqlInsert.EX_I(self.MainWindow.SqlConn, SQL_sentence)
        self.close()
    
    def actionButtonCancel(self):
        if self.mode == "Login":
            self.MainWindow.id_pwd[2] = self.MainWindow.id_pwd[3] = False
        self.close()

    def SetALLLLTextClear(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")

    def SetWindowMode(self, mode):
        self.mode = mode
        _translate = QtCore.QCoreApplication.translate
        if mode == "Login":
            self.MainWindow.id_pwd[2] = self.MainWindow.id_pwd[3] = False
            self.setWindowTitle(_translate("Form", "Login Window"))
        elif mode == "Register":
            self.setWindowTitle(_translate("Form", "Register Window"))

    def show(self) -> None:
        return super().show()