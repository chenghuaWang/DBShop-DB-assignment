"""
@Author:    chenghua.Wang
@file:      src/GUI/main_ui.py
@brief:     Main window of Qt   
"""

import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLabel, QMainWindow, QMessageBox, QSpinBox, QWidget, qApp, QHeaderView, QInputDialog
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import API.StyleModel as StyleModel  # TODO delete this  line in release mode

class UI_MainWindow():
    def __init__(self, MainWindow, SqlConn):
        self.MainWindow = MainWindow
        self.SqlConn = SqlConn
        self.Qw = QWidget()
        self.setupUi(self.MainWindow)
        # -- UI Show
        self.MainWindow.show()
        # -- Check Sql Link is ok
        if self.SqlConn.Status == True:
            QMessageBox.information(self.Qw,'Sql Link status',
                        'Sql Link Success',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        else:
            QMessageBox.information(self.Qw,'Sql Link status',
                        'Sql Link Error',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1429, 862)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView, 0, QtCore.Qt.AlignHCenter)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1429, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSearch = QtWidgets.QAction(MainWindow)
        self.actionSearch.setObjectName("actionSearch")
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.menu.addAction(self.actionQuit)
        self.menu.addAction(self.actionSearch)
        self.menu_2.addAction(self.actionLogin)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "&文件"))
        self.menu_2.setTitle(_translate("MainWindow", "账户管理"))
        # -- Quit.
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionQuit.setStatusTip(_translate("MainWindow", "Quit this window"))
        self.actionQuit.triggered.connect(qApp.quit)
        # -- Search.
        self.actionSearch.setText(_translate("MainWindow", "Search"))
        self.actionSearch.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSearch.setStatusTip(_translate("MainWindow", "Search in sql or script defined"))
        # -- Login.
        r"""
        User should first login.
        Use User_id or Shop_id or rootid to sign in.
        --
        First. Login will show a dialog and you should enter the info.
        """
        self.actionLogin.setText(_translate("MainWindow", "Login"))
        self.actionLogin.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionLogin.setStatusTip(_translate("MainWindow", "Login. User or root-Manager"))
        self.actionLogin.triggered.connect(lambda: self.LoginWindowShow())

    # -- Login Window Action Maker
    def LoginWindowShow(self):
        # TODO
        ID, ok_id = QInputDialog.getText(self.Qw, 'ID Input Dialog', 'Enter your ID:')
        if ok_id:
            Pwd, ok_pwd = QInputDialog.getText(self.Qw, 'pwd Input Dialog', 'Enter your password:')

    # -- Table View Action Maker
    def TableViewUpdate(self):
        # TODO
        # Reference: https://blog.csdn.net/jia666666/article/details/81624259
        # Reference button: https://blog.csdn.net/yy123xiang/article/details/78777964
        model=QStandardItemModel(4,4)
        model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])
        for row in range(4):
            for column in range(4):
                item=QStandardItem('row %s,column %s'%(row,column))
                model.setItem(row,column,item)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
