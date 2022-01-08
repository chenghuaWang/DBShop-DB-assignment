"""
@Author:    chenghua.Wang
@file:      src/GUI/API/main_window.py
@brief:     Main window of Qt   
"""

import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStyleFactory, QMessageBox, QMenu, QWidget, qApp, QInputDialog
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor

from GUI.API.Sql2Qt_Layer import LoginSqlAction, TreeViewSqlAction, MenuInsertSqlAction, LineEditSqlAction
from GUI.API.UserStatus import UserStatus_DS
from GUI.API.TableSqlAction import TableSqlAction
from GUI.API.CurrentTableStatus import CurrentTableStatus
from GUI.API.SearchTable_window import SearchTable_Window
from GUI.API.Inert_window import Insert_Window
from GUI.API.select_window import Select_Window
from GUI.API.Sql2Qt_Layer import SelectSqlAction
from GUI.API.Sql2Qt_Layer import LoginSqlAction_new
from GUI.API.Sql2Qt_Layer import RegisterSqlAction
from GUI.API.login_register_window import Login_Register_Window

class UI_MainWindow():
    def __init__(self, MainWindow, SqlConn):
        self.Insert_childWindow = Insert_Window(TableSqlAction, self)
        self.SearchTable_childWindow = SearchTable_Window()
        self.Select_childWindow = Select_Window(self, TableSqlAction)
        self.Login_Register_childWindow = Login_Register_Window(self, TableSqlAction, LoginSqlAction)
        self.TableStatus = CurrentTableStatus("default")
        self.UserStatus = UserStatus_DS("default", "default")
        self.id_pwd = ["default", "default", True, True]
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
        # -- Line Edit
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(lambda:LineEditSqlAction.main(self))
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # -- TreeView
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView, 0, QtCore.Qt.AlignHCenter)
        self.TreeViewInit(MainWindow)
        # -- TableView
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)  # set right menu start.
        self.tableView.customContextMenuRequested.connect(self.TableshowContextMenu)
        self.tableView.setSortingEnabled(True)
        self.horizontalLayout.addWidget(self.tableView)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1429, 26))
        self.menubar.setObjectName("menubar")
        # -- menu Bar
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        
        # -- Status Bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # -- action
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSearch = QtWidgets.QAction(MainWindow)
        self.actionSearch.setObjectName("actionSearch")
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionAddCUser = QtWidgets.QAction(MainWindow)
        self.actionAddCUser.setObjectName("actionAddCUser")
        self.actionAddPUser = QtWidgets.QAction(MainWindow)
        self.actionAddPUser.setObjectName("actionAddPUser")
        self.actionSort = QtWidgets.QAction(MainWindow)
        self.actionSort.setObjectName("actionSort")
        self.actionInsert = QtWidgets.QAction(MainWindow)
        self.actionInsert.setObjectName("actionInsert")
        # -- menu action
        self.menu.addAction(self.actionQuit)
        self.menu_2.addAction(self.actionLogin)
        self.menu_2.addAction(self.actionAddCUser)
        self.menu_2.addAction(self.actionAddPUser)
        self.menu_3.addAction(self.actionSort)
        self.menu_3.addAction(self.actionSearch)
        self.menu_3.addAction(self.actionInsert)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "&文件"))
        self.menu_2.setTitle(_translate("MainWindow", "账户管理"))
        self.menu_3.setTitle(_translate("MainWindow", "工具栏"))
        # -- Quit.
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionQuit.setStatusTip(_translate("MainWindow", "Quit this window"))
        self.actionQuit.triggered.connect(qApp.quit)
        # -- Search.
        self.actionSearch.setText(_translate("MainWindow", "查询"))
        self.actionSearch.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSearch.setStatusTip(_translate("MainWindow", "Use lambda function to get result"))
        self.actionSearch.triggered.connect(lambda: SelectSqlAction.main(self))
        # -- Sort
        self.actionSort.setText(_translate("MainWindow", "排序"))
        self.actionSort.setStatusTip(_translate("MainWindow", "sort in oreder"))
        # -- insert
        self.actionInsert.setText(_translate("MainWindow", "插入"))
        self.actionInsert.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionInsert.setStatusTip(_translate("MainWindow", "Insert into Table"))
        self.actionInsert.triggered.connect(lambda:MenuInsertSqlAction.main(self))
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
        # -- Add User
        self.actionAddCUser.setText(_translate("MainWindow", "Add custom User"))
        self.actionAddCUser.setStatusTip(_translate("MainWindow", "AddUser in C table"))
        self.actionAddCUser.triggered.connect(lambda: RegisterSqlAction.main(self, "C"))
        self.actionAddPUser.setText(_translate("MainWindow", "Add provider User"))
        self.actionAddPUser.setStatusTip(_translate("MainWindow", "AddUser in P table"))
        self.actionAddPUser.triggered.connect(lambda: RegisterSqlAction.main(self, "GG"))

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
        item_child_D = QStandardItem('D')
        item_project.appendRow(item_child_D)
        item_project.setChild(4, 1, QStandardItem('订单表'))
        # -- General set
        self.treeView.setModel(tree_model)
        self.treeView.expandAll()
        self.treeView.setStyle(QStyleFactory.create('windows'))
        self.treeView.selectionModel().currentChanged.connect(self.onCurrentChanged)
        # -- Add double click action
        self.treeView.clicked.connect(self.TreeViewClickedAction)

    # -- TreeView Init Action
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

    # -- TreeView clicked Action
    def TreeViewClickedAction(self, QModelidx):
        TreeViewSqlAction.main(self, QModelidx)

    # -- Login Window Action Maker
    def LoginWindowShow(self):
        LoginSqlAction_new.main(self)
        """print(self.id_pwd)
        ok_id = ok_pwd = False
        ID, ok_id = QInputDialog.getText(self.Qw, 'ID Input Dialog', 'Enter your ID:')
        if ok_id:
            if ID[0] in ['C', 'P', 'r'] and ID != "":
                Pwd, ok_pwd = QInputDialog.getText(self.Qw, 'pwd Input Dialog', 'Enter your password:')
            else:
                QMessageBox.information(self.Qw,'Error',"不存在用户{a}".format(a=ID),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if ok_id and ok_pwd:
            if ID[0] in ['C', 'P', 'r']:
                self.UserStatus.Update(ID[0], ID)
            LoginSqlAction.main(self, ID[0], ID, Pwd)"""
    
    def TableRightClick(self):
        TableSqlAction.TableViewRightClickMain(self)

    def TableLeftClick(self, QModelidx):
        print(QModelidx.row())

    def TableshowContextMenu(self, qt_point):
        """
        Create right click menu
        """
        TableSqlAction.TableRightMenuContent(self, qt_point)
