"""
@Author:    chenghua.Wang
@file:      src/GUI/main_ui.py
@brief:     Main window of Qt   
"""

import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStyleFactory, QDialogButtonBox, QFormLayout, QLabel, QMainWindow, QMessageBox, QSpinBox, QWidget, qApp, QHeaderView, QInputDialog
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from GUI.API.Sql2Qt_Layer import LoginSqlAction

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
        # -- TreeView
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView, 0, QtCore.Qt.AlignHCenter)
        self.TreeViewInit(MainWindow)
        # -- TreeView
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
    
    # -- TreeView
    def TreeViewInit(self, MainWindow):
        # -- Add head info
        tree_model = QStandardItemModel(MainWindow)
        tree_model.setHorizontalHeaderLabels(['数据库', '信息说明'])
        # -- Add Item
        item_project = QStandardItem('Shop')
        tree_model.appendRow(item_project)
        tree_model.setItem(0, 1, QStandardItem('商品数据库'))
        # -- Add Item in item_project
        item_child_C = QStandardItem('C')
        item_project.appendRow(item_child_C)
        item_project.setChild(0, 1, QStandardItem('客户信息'))
        item_child_S = QStandardItem('S')
        item_project.appendRow(item_child_S)
        item_project.setChild(1, 1, QStandardItem('商品表'))
        item_child_G = QStandardItem('G')
        item_project.appendRow(item_child_G)
        item_project.setChild(2, 1, QStandardItem('购物车表'))
        item_child_GG = QStandardItem('GG')
        item_project.appendRow(item_child_GG)
        item_project.setChild(3, 1, QStandardItem('商户表'))
        # -- General set
        self.treeView.setModel(tree_model)
        self.treeView.expandAll()
        self.treeView.setStyle(QStyleFactory.create('windows'))
        self.treeView.selectionModel().currentChanged.connect(self.onCurrentChanged)

    # -- TreeView Action
    def onCurrentChanged(self,current, previous):
        txt = '父级:[{}] '.format(str(current.parent().data()))
        txt += '当前选中:[(行{},列{})] '.format(current.row(), current.column())
        name=''
        info=''
        if current.column() == 0:
            name = str(current.data())
            info = str(current.sibling(current.row(), 1).data())
        else:
            name = str(current.sibling(current.row(), 0).data())
            info = str(current.data())
        
        txt += '名称:[{}]  信息:[{}]'.format(name, info)    
        self.statusbar.showMessage(txt)


    # -- Login Window Action Maker
    def LoginWindowShow(self):
        # TODO
        ID, ok_id = QInputDialog.getText(self.Qw, 'ID Input Dialog', 'Enter your ID:')
        if ok_id:
            Pwd, ok_pwd = QInputDialog.getText(self.Qw, 'pwd Input Dialog', 'Enter your password:')
        if ok_id and ok_pwd:
            # Create View first.
            self.LoginWindow_TableViewChange(ID, "G")
        else:
            pass
    
    def LoginWindow_TableViewChange(self, ID, TableName):
        data, describe = LoginSqlAction.GetUserTable(self.SqlConn, ID, TableName)
        #TODO
        pass

    # -- Table View Action Maker
    def TableViewUpdate(self, HeaderLabel, Data):
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
