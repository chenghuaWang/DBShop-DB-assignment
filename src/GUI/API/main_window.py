"""
@Author:    chenghua.Wang
@file:      src/GUI/main_ui.py
@brief:     Main window of Qt   
"""

import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import API.StyleModel as StyleModel  # TODO

class UI_MainWindow():
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
        self.actionLogin.setText(_translate("MainWindow", "Login"))
        self.actionLogin.triggered.connect(lambda: self.TableViewUpdate())

    def TableViewUpdate(self):
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

"""
# If you want to run this pro. you should use
    app = QApplication(sys.argv)
    StyleModel.style_modeling(app, 'dark_lightgreen.xml')
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    StyleModel.style_modeling(app, 'dark_blue.xml')
    MainWindow = QMainWindow()
    ui = UI_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

"""
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.__initGeometry__()
        self.__initTopbar__()
        
        self.setWindowTitle('PyQt5 Basic Menubar')    
        self.show()

    def __initGeometry__(self):
        desktop_size = QApplication.desktop()
        self.w = desktop_size.width() //2
        self.h = desktop_size.height() // 2
        x = self.w // 2
        y = self.h // 2
        self.setGeometry(x, y, self.w, self.h)

    def __initTopbar__(self):
        # -- File Bar
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        searchAction = QAction('&search', self)
        searchAction.setShortcut('Ctrl+S')
        searchAction.setStatusTip('Use sql to search')
        searchAction.triggered.connect(lambda:self.searchbar_line_edit())

        FontAction = QAction('&Font', self)
        FontAction.setStatusTip('Font setting')
        FontAction.triggered.connect(lambda:self.DialogFont())

        # self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(searchAction)
        fileMenu.addAction(FontAction)
        # -- Bar Bar

    def __initTabel__():
        pass

    def searchbar_line_edit(self):
        StringLine = QLineEdit(self)
        StringLine.resize(self.w, 30)
        StringLine.move(0, self.h-30)
        # TODO
        StringLine.show()

    def DialogFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.setFont(font)


    def changeTitle(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')
"""

