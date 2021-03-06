"""
@Author:    chenghua.Wang
@file:      src/GUI/API/Inert_window.py
@brief:     Insert window for MainWindow class.
"""
import os
import sys
import time;
import calendar;
sys.path.append(os.path.split(sys.path[0])[0])

import logging
logging.getLogger().setLevel(logging.DEBUG)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QMessageBox, QTableWidget, QWidget, qApp, QInputDialog
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor

from core.SqlMan import SqlSearch_DS
from logic.SqlInsert import SqlInsert

class Insert_Window(QtWidgets.QDialog):
    def __init__(self, func_cls, MainWindow):
        super().__init__()
        self.Qw = QWidget()
        self.setupUi()
        self.TableData = []
        self.TableDescribe = []
        self.func_cls = func_cls
        self.MainWindow = MainWindow
        
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(974, 712)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout.addWidget(self.tableWidget)
        self.AddItemButton = QtWidgets.QPushButton(self)
        self.AddItemButton.setObjectName("AddItemButton")
        self.verticalLayout.addWidget(self.AddItemButton)
        self.SubmitButton = QtWidgets.QPushButton(self)
        self.SubmitButton.setObjectName("SubmitButton")
        self.verticalLayout.addWidget(self.SubmitButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.AddItemButton.setText(_translate("Form", "????????????"))
        self.AddItemButton.clicked.connect(self.AddItemButton_action)
        self.SubmitButton.setText(_translate("Form", "??????"))
        self.SubmitButton.clicked.connect(self.SubmitButton_action)
    
    def itemChangeAction(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("------------>",id)
    
    def initData(self):
        """
        U should use this function to init data and describe.
        VERY VITAL SIGNIFICANT.
        """
        self.TableDescribe = self.MainWindow.TableStatus.describe
        _buf_tuple_ = ()
        for idx in self.TableDescribe:
            _buf_tuple_ = _buf_tuple_ + (" ", )
        self.TableData = SqlSearch_DS([_buf_tuple_])
        self.UpdateTableData(self.TableData, self.TableDescribe)

    def AddItemButton_action(self):
        NumCol = self.TableData.NumCol
        NumRow = self.TableData.NumRow
        self.TableData.m_row.pop(0)
        _buf_tuple_ = ()
        for idx in range(0, NumCol):
            _buf_tuple_ = _buf_tuple_ + (self.tableWidget.item(0, idx).text(), )
            # self.TableData.m_row[0][idx] = self.tableWidget.item(0, idx).text()
        self.TableData.m_row.insert(0, _buf_tuple_)
        self.TableDescribe = self.MainWindow.TableStatus.describe
        _buf_tuple_2 = ()
        for idx in self.TableDescribe:
            _buf_tuple_2 = _buf_tuple_2 + (" ", )
        self.TableData.m_row = [_buf_tuple_2] + self.TableData.m_row
        # self.TableData.m_row.insert(0, _buf_tuple_2)
        print(self.TableData.NumRow)
        self.UpdateTableData(self.TableData, self.TableDescribe)

    def SubmitButton_action(self):
        """
        First check first line of data is empty or not.
        """
        SQL_Sentence = []
        StartRow = 0
        if self.tableWidget.item(0, 0).text() == "":
            StartRow = 1
        else:
            self.AddItemButton_action()
            StartRow = 1
            if self.MainWindow.TableStatus.TableName == "S":
                """
                ?????????root, P???????????????????????? S insert enable
                """
                for idx in range(StartRow, self.TableData.NumRow_f()):
                    _buf_value_ = "('{a}','{b}','{c}',{d},{e})".format(
                        a=self.TableData.m_row[idx][0],
                        b=self.TableData.m_row[idx][1],
                        c=self.TableData.m_row[idx][2],
                        d=self.TableData.m_row[idx][3],
                        e=self.TableData.m_row[idx][4]
                    )
                    _buf_sql_ = "insert into "+self.MainWindow.TableStatus.TableName+" VALUES"+_buf_value_
                    SQL_Sentence.append(_buf_sql_)
                """
                ?????????????????????????????????????????????GGS?????????????????????????????????GG???
                """
                if self.MainWindow.UserStatus.User_mode == "P":
                    for item in SQL_Sentence:
                        SqlInsert.EX_I(self.MainWindow.SqlConn,item)
                    SqlInsert.EX_I(self.MainWindow.SqlConn, "insert into GGS VALUES('{a}','{b}')".format(
                        a=self.TableData.m_row[idx][0],
                        b=self.MainWindow.UserStatus.User_info
                    ))
                else:
                    for item in SQL_Sentence:
                        logging.info(item)
                        SqlInsert.EX_I(self.MainWindow.SqlConn,item)
            elif self.MainWindow.TableStatus.TableName == "GG":
                for idx in range(StartRow, self.TableData.NumRow_f()):
                    _buf_value_ = "('{a}','{b}','{c}')".format(
                        a=self.TableData.m_row[idx][0],
                        b=self.TableData.m_row[idx][1],
                        c=self.TableData.m_row[idx][2],
                    )
                    _buf_sql_ = "insert into "+self.MainWindow.TableStatus.TableName+" VALUES"+_buf_value_
                    SQL_Sentence.append(_buf_sql_)
                    for item in SQL_Sentence:
                        SqlInsert.EX_I(self.MainWindow.SqlConn,item)
            elif self.MainWindow.TableStatus.TableName == "D":
                for idx in range(StartRow, self.TableData.NumRow_f()):
                    _buf_value_ = "('{a}','{b}',{c},{d},{e},{f})".format(
                        a=self.TableData.m_row[idx][0],
                        b=self.TableData.m_row[idx][1],
                        c=self.TableData.m_row[idx][2],
                        d=self.TableData.m_row[idx][3],
                        e=self.TableData.m_row[idx][4],
                        f=self.TableData.m_row[idx][5],
                    )
                    _buf_sql_ = "insert into "+self.MainWindow.TableStatus.TableName+" VALUES"+_buf_value_
                    SQL_Sentence.append(_buf_sql_)
                    for item in SQL_Sentence:
                        SqlInsert.EX_I(self.MainWindow.SqlConn,item)
            elif self.MainWindow.TableStatus.TableName == "C":
                for idx in range(StartRow, self.TableData.NumRow_f()):
                    _buf_value_ = "('{a}','{b}','{c}','{d}')".format(
                        a=self.TableData.m_row[idx][0],
                        b=self.TableData.m_row[idx][1],
                        c=self.TableData.m_row[idx][2],
                        d=self.TableData.m_row[idx][3],
                    )
                    _buf_sql_ = "insert into "+self.MainWindow.TableStatus.TableName+" VALUES"+_buf_value_
                    SQL_Sentence.append(_buf_sql_)
                    _buf_sql1_ = "insert into G values('{a}','{b}')".format(
                        a="G"+str(calendar.timegm(time.gmtime()))[0:8],
                        b=self.TableData.m_row[idx][0]
                    ) 
                    SQL_Sentence.append(_buf_sql1_)
                    for item in SQL_Sentence:
                        SqlInsert.EX_I(self.MainWindow.SqlConn,item)
            elif self.MainWindow.TableStatus.TableName == "G":
                pass
            self.func_cls.TableFlushes(self.MainWindow)
            self.close()
        
    def UpdateTableData(self, Data, HeaderLabel):
        if Data.NumRow_f() == 0:
            QMessageBox.information(self.Qw,'Search Failed',
                        "Table Don't have data matched!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        self.tableWidget.setColumnCount(Data.NumCol)
        self.tableWidget.setRowCount(Data.NumRow_f())
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setHorizontalHeaderLabels(HeaderLabel)
        self.tableWidget.verticalHeader().setVisible(False)
        for row in range(Data.NumRow_f()):
            for column in range(Data.NumCol):
                item = QtWidgets.QTableWidgetItem("{a}".format(a=Data.GetSingleData(row, column)).encode('latin1').decode('gbk'))
                item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable)
                self.tableWidget.setItem(row,column,item)

    def show(self) -> None:
        return super().show()
