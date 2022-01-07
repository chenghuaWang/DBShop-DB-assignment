"""
@Author:    chenghua.Wang
@file:      src/GUI/TableSqlAction.py
@brief:     Table Action Logic. Independent.
"""
import logging
import os
from string import ascii_uppercase
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMessageBox, QMenu, QWidget, qApp, QInputDialog
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor

from logic.SqlDelete import SqlDelete

class TableSqlAction:
    @staticmethod
    def TableViewUpdate(MainWindow, HeaderLabel, Data):
        # TODO
        # Reference: https://blog.csdn.net/jia666666/article/details/81624259
        # Reference button: https://blog.csdn.net/yy123xiang/article/details/78777964
        # U should use `.encode('latin1').decode('gbk')` to get correct characters.
        if Data.NumRow == 0:
            QMessageBox.information(MainWindow.Qw,'Search Failed',
                        "Table Don't have data matched!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        model=QStandardItemModel(Data.NumRow, Data.NumCol)
        model.setHorizontalHeaderLabels(HeaderLabel)
        for row in range(Data.NumRow):
            for column in range(Data.NumCol):
                item=QStandardItem("{a}".format(a=Data.GetSingleData(row, column)).encode('latin1').decode('gbk'))
                model.setItem(row,column,item)
        MainWindow.tableView.setModel(model)
        MainWindow.tableView.horizontalHeader().setStretchLastSection(True)
        MainWindow.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    @staticmethod
    def TableViewRightClick_deleteOne(MainWindow):
        r"""
        Delete function for "G"\"D" Table only.
        """
        pass

    @staticmethod
    def TableViewRightClick_deleteMulti(MainWindow):
        pass

    @staticmethod
    def TableViewRightClick_deleteAll(MainWindow):
        pass

    @staticmethod
    def TableViewRightClick_insert(MainWindow):
        """
        Will open a Window reference to Whitch item this table have.
        """
        pass

    @staticmethod
    def TableRightMenuContent(MainWindow, qt_point):
        qt_Modleidx = QtWidgets.QTableView.indexAt(MainWindow.tableView,qt_point)
        # print(qt_Modleidx.row(), qt_Modleidx.column())
        MainWindow.tableView.contextMenu = QMenu(MainWindow.Qw)
        """
        All Table is "C", "S", "G", "GG", "D"
        Build numerous Action for different Table and User.
        1. "C" Login.
        "C" -> RightClick Disable.
        "S" -> Can Add item into "G" table.
            -> 1. Add 1 item into "G" table
            -> 2. Add Multi Item into "G" table
        "G" -> 1. Delete 1 item from "G" table. if item_num == 0, delete this data.
            -> 2. Delete Multi item from "G" table. Need to check Item_num is right.
            -> 3. Search for Supporter(GG)
        "GG"-> RightClick Disable
        "D" -> RightClick Disable

        2. "P" Login
        "C" -> Can not reach
        "S" -> 1. Can delete self-shop
        "G" -> Can not reach
        "GG"-> RightClick Disable
        "D" -> RightClick Disable

        3. "r" Login
        Can delete All Item from every table. 
        """
        if MainWindow.UserStatus.User_mode == "C":
            if MainWindow.TableStatus.TableName == "C":
                pass
            elif MainWindow.TableStatus.TableName == "S":
                MainWindow.actionAdd2G_one = MainWindow.tableView.contexMenu.addAction(r"添加一件到购物车")
                # TODO add function
                MainWindow.actionAdd2G_multi = MainWindow.tableView.contexMenu.addAction(r"添加多项到购物车")
                # TODO add function
                MainWindow.actionSearchSupportor = MainWindow.tableView.contexMenu.addAction(r"查找供应商")
                #TODO Add function
            elif MainWindow.TableStatus.TableName == "G":
                MainWindow.actionDelete_one  = MainWindow.tableView.contexMenu.addAction(r"删除一项")
                # TODO delete function
                MainWindow.actionDelete_all = MainWindow.tableView.contexMenu.addAction(r"删除多项")
                # TODO delete function
                MainWindow.actionSearchSupportor = MainWindow.tableView.contexMenu.addAction(r"查找供应商")
                # Add function

        
        # MainWindow.actionDelete = MainWindow.tableView.contextMenu.addAction(r"删除一项")
        # MainWindow.actionDelete.triggered.connect(lambda:TableSqlAction.TableViewRightClick_deleteOne(MainWindow))
        MainWindow.tableView.contextMenu.popup(QCursor.pos())  # Position of menu
        MainWindow.tableView.contextMenu.show()
