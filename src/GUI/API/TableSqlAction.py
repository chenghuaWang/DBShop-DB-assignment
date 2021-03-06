"""
@Author:    chenghua.Wang
@file:      src/GUI/TableSqlAction.py
@brief:     Table Action Logic. Independent.
"""
import os
from re import M
import sys
import time
import calendar

from src.logic.SqlInsert import SqlInsert
sys.path.append(os.path.split(sys.path[0])[0])

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMessageBox, QMenu, QWidget, qApp, QInputDialog
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor

from logic.SqlDelete import SqlDelete
from logic.SqlSearch import SqlSearch
from logic.SqlChange import SqlChange
from logic.SqlInsert import SqlInsert

from GUI.API.SearchTable_window import SearchTable_Window

class TableSqlAction:
    @staticmethod
    def TableViewUpdate(MainWindow, HeaderLabel, Data):
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
    def TableViewRightClick_Push2D(MainWindow, qt_Modelidx):
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        # Get All item in G's index and info
        G_items = MainWindow.TableStatus.data.m_row
        G_items_discribe = MainWindow.TableStatus.describe
        # Get All info and insert into D,DS Table
        SPrice = 0
        DNo_buf = "D" + str(calendar.timegm(time.gmtime()))[0:8]
        for idx in range(0, len(G_items)):
            SPrice += (G_items[idx][G_items_discribe.index("SPrice")]) * (G_items[idx][G_items_discribe.index("GSNum")])
        D_value = "'{DNo}', '{CNo}', {DPay}, {DPay_yn}, {DS_yn}, {DM_yn}".format(
            DNo=DNo_buf,
            CNo=MainWindow.UserStatus.User_info,
            DPay=SPrice,
            DPay_yn='1',
            DS_yn='0',
            DM_yn='0.0'
        )
        SQL_sentence = "insert into D values({a})".format(a=D_value)
        SqlInsert.EX_I(MainWindow.SqlConn, SQL_sentence)
        for idx in range(0, len(G_items)):
            # insert to DS
            SQL_sentence = "insert into DS values('{SNo}','{DNo}',{DSNum});".format(
                SNo=G_items[idx][G_items_discribe.index("SNo")],
                DNo=DNo_buf,
                DSNum=G_items[idx][G_items_discribe.index("GSNum")]
            )
            SqlInsert.EX_I(MainWindow.SqlConn, SQL_sentence)
        # Delete all item in G
        SQL_sentence = "delete from G where GNo='{a}';".format(
            a=G_items[0][G_items_discribe.index("GNo")]
        )
        SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)

        TableSqlAction.TableFlushes(MainWindow)

    @staticmethod
    def TableViewRightClick_Add2G_one(MainWindow, qt_Modelidx):
        """
        This function has already be Checked by menu logic.
        And it can only be visited by Custom Login.
        """
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        SNo_idx_in_S = MainWindow.TableStatus.describe.index("SNo")
        _buf_SNo = MainWindow.TableStatus.data.m_row[row][SNo_idx_in_S]
        # Search GNo.
        GNo_searched = SqlSearch.SelfDefind_S_direct(
            MainWindow.SqlConn,
            "select GNo from G where CNo='{a}'".format(a=MainWindow.UserStatus.User_info)
        )
        if GNo_searched.NumRow_f() == 0:
            _buf_sql1_ = "insert into G values('{a}','{b}')".format(
                a="G"+str(calendar.timegm(time.gmtime()))[0:8],
                b=MainWindow.UserStatus.User_info
            )
            SqlInsert.EX_I(MainWindow.SqlConn, _buf_sql1_)
            GNo_searched = SqlSearch.SelfDefind_S_direct(
                MainWindow.SqlConn,
                "select GNo from G where CNo='{a}'".format(a=MainWindow.UserStatus.User_info)
            )
        GNo_searched = GNo_searched.m_row[0][0]
        # Get whether This item is exists.
        SQL_sentence = "select GSNum from GS where GNo='{a}' and SNo='{b}';".format(
            a=GNo_searched,
            b=_buf_SNo,    
        )
        Num_seqrched = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_sentence)
        # debug->print(Num_seqrched.NumRow_f(), Num_seqrched.m_row)
        if Num_seqrched.NumRow_f() == 0:
            SQL_sentence = "insert into GS values('{a}', '{b}', {c});".format(
                a=_buf_SNo,
                b=GNo_searched,
                c=1
            )
            SqlInsert.EX_I(MainWindow.SqlConn, SQL_sentence)
        else:
            SQL_sentence = "update GS set GSNum={a} where GNo='{b}' and SNo='{c}';".format(
                a=Num_seqrched.m_row[0][0] + 1,
                b=GNo_searched,
                c=_buf_SNo
            )
            SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)

    @staticmethod
    def TableViewRightClick_Add2G_multi(MainWindow, qt_Modelidx):
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        SNo_idx_in_S = MainWindow.TableStatus.describe.index("SNo")
        _buf_SNo = MainWindow.TableStatus.data.m_row[row][SNo_idx_in_S]
        Num, ok_Num = QInputDialog.getInt(MainWindow.Qw, 'Num Input Dialog', 'Enter Number:')
        if ok_Num == False or int(Num) <= 0:
            return
        # Search GNo.
        GNo_searched = SqlSearch.SelfDefind_S_direct(
            MainWindow.SqlConn,
            "select GNo from G where CNo='{a}'".format(a=MainWindow.UserStatus.User_info)
        )
        if GNo_searched.NumRow_f() == 0:
            _buf_sql1_ = "insert into G values('{a}','{b}')".format(
                a="G"+str(calendar.timegm(time.gmtime()))[0:8],
                b=MainWindow.UserStatus.User_info
            )
            SqlInsert.EX_I(MainWindow.SqlConn, _buf_sql1_)
            GNo_searched = SqlSearch.SelfDefind_S_direct(
                MainWindow.SqlConn,
                "select GNo from G where CNo='{a}'".format(a=MainWindow.UserStatus.User_info)
            )
        GNo_searched = GNo_searched.m_row[0][0]
        # Get whether This item is exists.
        SQL_sentence = "select GSNum from GS where GNo='{a}' and SNo='{b}';".format(
            a=GNo_searched,
            b=_buf_SNo,    
        )
        Num_seqrched = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_sentence)
        # debug->print(Num_seqrched.NumRow_f(), Num_seqrched.m_row)
        if Num_seqrched.NumRow_f() == 0:
            SQL_sentence = "insert into GS values('{a}', '{b}', {c});".format(
                a=_buf_SNo,
                b=GNo_searched,
                c=Num
            )
            SqlInsert.EX_I(MainWindow.SqlConn, SQL_sentence)
        else:
            SQL_sentence = "update GS set GSNum={a} where GNo='{b}' and SNo='{c}';".format(
                a=Num_seqrched.m_row[0][0] + Num,
                b=GNo_searched,
                c=_buf_SNo
            )
            SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)

    @staticmethod
    def TableViewRightClick_deleteOne(MainWindow, qt_Modelidx, Primary_Key_Name):
        r"""
        This function has already be Checked by menu logic.
        Delete function for "G"\"D" Table only.
        """
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        if MainWindow.TableStatus.TableName == "G" and MainWindow.UserStatus.User_mode=="C":
            SNo_idx_in_S = MainWindow.TableStatus.describe.index("SNo")
            _buf_SNo = MainWindow.TableStatus.data.m_row[row][SNo_idx_in_S]
            # Search GNo.
            GNo_searched = SqlSearch.SelfDefind_S_direct(
                MainWindow.SqlConn,
                "select GNo from G where CNo='{a}'".format(a=MainWindow.UserStatus.User_info)
            )
            GNo_searched = GNo_searched.m_row[0][0]
            # Get whether This item is exists.
            SQL_sentence = "select GSNum from GS where GNo='{a}' and SNo='{b}';".format(
                a=GNo_searched,
                b=_buf_SNo,    
            )
            Num_seqrched = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_sentence)
            # debug->print(Num_seqrched.NumRow_f(), Num_seqrched.m_row)
            if Num_seqrched.m_row[0][0] == 1:
                SQL_sentence = "delete from GS where SNo='{a}' and GNo='{b}'".format(
                    a=_buf_SNo,
                    b=GNo_searched
                )
                SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)
            else:
                SQL_sentence = "update GS set GSNum={a} where GNo='{b}' and SNo='{c}';".format(
                    a=Num_seqrched.m_row[0][0] - 1,
                    b=GNo_searched,
                    c=_buf_SNo
                )
                SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)
        elif MainWindow.TableStatus.TableName == "D" and MainWindow.UserStatus.User_mode=="C":
            SNo_idx_in_S = MainWindow.TableStatus.describe.index("SNo")
            _buf_SNo = MainWindow.TableStatus.data.m_row[row][SNo_idx_in_S]
            # Search DNo.
            DNo_searched = MainWindow.TableStatus.data.m_row[row][MainWindow.TableStatus.describe.index("DNo")]
            # Get whether This item is exists.
            SQL_sentence = "select DSNum from DS where DNo='{a}' and SNo='{b}';".format(
                a=DNo_searched,
                b=_buf_SNo,    
            )
            print(SQL_sentence)
            Num_seqrched = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_sentence)
            # debug->print(Num_seqrched.NumRow_f(), Num_seqrched.m_row)
            if Num_seqrched.m_row[0][0] == 1:
                SQL_sentence = "delete from DS where SNo='{a}' and DNo='{b}'".format(
                    a=_buf_SNo,
                    b=DNo_searched
                )
                SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)
            else:
                SQL_sentence = "update DS set DSNum={a} where DNo='{b}' and SNo='{c}';".format(
                    a=Num_seqrched.m_row[0][0] - 1,
                    b=DNo_searched,
                    c=_buf_SNo
                )
                SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)
        else:
            Table_in_sql = MainWindow.TableStatus.TableName
            Primary_key_idx_in_table = MainWindow.TableStatus.describe.index(Primary_Key_Name)
            Primary_key_value = MainWindow.TableStatus.data.m_row[row][Primary_key_idx_in_table]
            # check num is 1 or not, delete if num is 1, else update
            SQL_sentence = "select "
            # execute delete one logic
            SQL_sentence = "delete from {a} where {b}='{c}'".format(
                a=Table_in_sql,
                b=Primary_Key_Name,
                c=Primary_key_value
            )
            SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)
        TableSqlAction.TableFlushes(MainWindow)

    @staticmethod
    def TableViewRightClick_deleteMulti(MainWindow, qt_Modelidx, Primary_Key_Name):
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        Num, ok_Num = QInputDialog.getInt(MainWindow.Qw, 'Num Input Dialog', 'Enter Number:')
        if ok_Num == False or int(Num) <= 0:
            return
        if MainWindow.TableStatus.TableName == "G" and MainWindow.UserStatus.User_mode=="C":
            SNo_idx_in_S = MainWindow.TableStatus.describe.index("SNo")
            _buf_SNo = MainWindow.TableStatus.data.m_row[row][SNo_idx_in_S]
            # Search GNo.
            GNo_searched = SqlSearch.SelfDefind_S_direct(
                MainWindow.SqlConn,
                "select GNo from G where CNo='{a}'".format(a=MainWindow.UserStatus.User_info)
            )
            GNo_searched = GNo_searched.m_row[0][0]
            # Get whether This item is exists.
            SQL_sentence = "select GSNum from GS where GNo='{a}' and SNo='{b}';".format(
                a=GNo_searched,
                b=_buf_SNo,    
            )
            Num_seqrched = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_sentence)
            # debug->print(Num_seqrched.NumRow_f(), Num_seqrched.m_row)
            if Num_seqrched.m_row[0][0] == Num:
                SQL_sentence = "delete from GS where SNo='{a}' and GNo='{b}'".format(
                    a=_buf_SNo,
                    b=GNo_searched
                )
                SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)
            else:
                SQL_sentence = "update GS set GSNum={a} where GNo='{b}' and SNo='{c}';".format(
                    a=Num_seqrched.m_row[0][0] - Num,
                    b=GNo_searched,
                    c=_buf_SNo
                )
                SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)
        elif MainWindow.TableStatus.TableName == "D" and MainWindow.UserStatus.User_mode=="C":
            SNo_idx_in_S = MainWindow.TableStatus.describe.index("SNo")
            _buf_SNo = MainWindow.TableStatus.data.m_row[row][SNo_idx_in_S]
            # Search DNo.
            DNo_searched = MainWindow.TableStatus.data.m_row[row][MainWindow.TableStatus.describe.index("DNo")]
            # Get whether This item is exists.
            SQL_sentence = "select DSNum from DS where DNo='{a}' and SNo='{b}';".format(
                a=DNo_searched,
                b=_buf_SNo,    
            )
            Num_seqrched = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_sentence)
            # debug->print(Num_seqrched.NumRow_f(), Num_seqrched.m_row)
            if Num_seqrched.m_row[0][0] == Num:
                SQL_sentence = "delete from DS where SNo='{a}' and DNo='{b}'".format(
                    a=_buf_SNo,
                    b=DNo_searched
                )
                SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)
            else:
                SQL_sentence = "update DS set DSNum={a} where DNo='{b}' and SNo='{c}';".format(
                    a=Num_seqrched.m_row[0][0] - Num,
                    b=DNo_searched,
                    c=_buf_SNo
                )
                SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)
        else:
            Table_in_sql = MainWindow.TableStatus.TableName
            Primary_key_idx_in_table = MainWindow.TableStatus.describe.index(Primary_Key_Name)
            Primary_key_value = MainWindow.TableStatus.data.m_row[row][Primary_key_idx_in_table]
            # check num is 1 or not, delete if num is 1, else update
            SQL_sentence = "select "
            # execute delete one logic
            SQL_sentence = "delete from {a} where {b}='{c}'".format(
                a=Table_in_sql,
                b=Primary_Key_Name,
                c=Primary_key_value
            )
            SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)
        TableSqlAction.TableFlushes(MainWindow)

    @staticmethod
    def TableViewRightClick_deleteAll(MainWindow, qt_Modelidx, Primary_Key_Name):
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        if MainWindow.TableStatus.TableName == "G":
            Table_in_sql = "GS"
        elif MainWindow.TableStatus.TableName == "D":
            Table_in_sql = "DS"
        else:
            Table_in_sql = MainWindow.TableStatus.TableName
        Primary_key_idx_in_table = MainWindow.TableStatus.describe.index(Primary_Key_Name)
        Primary_key_value = MainWindow.TableStatus.data.m_row[row][Primary_key_idx_in_table]
        SQL_sentence = "delete from {a} where {b}='{c}'".format(
            a=Table_in_sql,
            b=Primary_Key_Name,
            c=Primary_key_value
        )
        SqlDelete.EX_D(MainWindow.SqlConn, SQL_sentence)
        TableSqlAction.TableFlushes(MainWindow)

    @staticmethod
    def TableViewRightClick_insert(MainWindow):
        """
        Will open a Window reference to Whitch item this table have.
        """
        pass

    @staticmethod
    def TableViewRightClick_SearchSupportor(MainWindow, qt_Modelidx):
        """
        This function only show in Table G and S.
        In S Table col of SNo is 0,
        In G Table col of SNo is 2.
        """
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        SNo_idx_in_S = MainWindow.TableStatus.describe.index("SNo")
        _buf_SNo = MainWindow.TableStatus.data.m_row[row][SNo_idx_in_S]
        _buf_need = "GG.GGNo, GG.GGName, GG.GGAddr, S.SNo, S.SName"
        SQL_Sentence = "select {need} from S,GG,GGS where S.SNo='{a}' and GGS.GGNo=GG.GGNo and GGS.SNo=S.SNo;".format(
            need = _buf_need,
            a=_buf_SNo
        )
        _data_ = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn,SQL_Sentence)
        _describe_ = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
        MainWindow.SearchTable_childWindow.UpdateTableData(TableSqlAction, _data_, _describe_)
        MainWindow.SearchTable_childWindow.show()

    @staticmethod
    def TableViewRightClick_Change(MainWindow, qt_Modelidx):
        """
        The No is always the first col of table.
        """
        row = qt_Modelidx.row()
        col = qt_Modelidx.column()
        Primary_index_name = MainWindow.TableStatus.TableName + "No"
        Key_want_change_name = MainWindow.TableStatus.describe[col]
        value, ok_value = QInputDialog.getText(MainWindow.Qw, 'Value change.', 'Enter new data:')
        if ok_value:
            try:
                SQL_sentence = "update {a} set {b}='{c}' where {d}='{e}';".format(
                    a=MainWindow.TableStatus.TableName,
                    b=Key_want_change_name,
                    c=value,
                    d=Primary_index_name,
                    e=MainWindow.TableStatus.data.m_row[row][0]
                )
                logging.error(SQL_sentence)
                SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)
            except:
                logging.error("try value type instead of string type")
                try:
                    SQL_sentence = "update {a} set {b}={c} where {d}='{e}';".format(
                        a=MainWindow.TableStatus.TableName,
                        b=Key_want_change_name,
                        c=value,
                        d=Primary_index_name,
                        e=MainWindow.TableStatus.data.m_row[row][0]
                    )
                    logging.error(SQL_sentence)
                    SqlChange.EX_C(MainWindow.SqlConn, SQL_sentence)
                except:
                    logging.error("SQL sentence error")
                    QMessageBox.information(MainWindow.Qw,'ERROR',
                        'Can not change due to some errors.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        # Flush window
        TableSqlAction.TableFlushes(MainWindow)

    @staticmethod
    def TableFlushes(MainWindow):
        table_name = MainWindow.TableStatus.TableName
        if MainWindow.UserStatus.User_mode == "r":
            if MainWindow.UserStatus.User_mode != "r":
                logging.error("User mode is changed when you clicked. Failed to load")
                QMessageBox.information(MainWindow.Qw,'MSG B',
                            "User mode is changed when you clicked. Failed to load!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            else:
                if table_name in ["C", "S", "GG", "D"]:
                    SQL_Sentence = "select * from {a};".format(a=table_name)
                elif table_name == "G":
                    _buf_col = "G.GNo,G.CNo,S.SNo,S.SName,S.SKind,S.SPrice,S.SInventory,GS.GSNum"
                    SQL_Sentence = "select {a} from G,C,GS,S where G.GNo=GS.GNo and GS.SNo=S.SNo and G.CNo=C.CNo;".format(a=_buf_col)
                data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
                description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
                TableSqlAction.TableViewUpdate(MainWindow, description, data)
                MainWindow.TableStatus.Update(table_name, data, description)
        elif MainWindow.UserStatus.User_mode == "C":
            if MainWindow.UserStatus.User_mode != 'C':
                logging.error("User mode is changed when you clicked. Failed to load")
                QMessageBox.information(MainWindow.Qw,'MSG B',
                            "User mode is changed when you clicked. Failed to load!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            else:
                if table_name == "C":
                    SQL_Sentence = "select * from C where CNo='{a}';".format(a=MainWindow.UserStatus.User_info)
                elif table_name == "G":
                    _buf_col = "G.GNo,C.CNo,S.SNo,S.SName,S.SKind,S.SPrice,S.SInventory,GS.GSNum"
                    SQL_Sentence = "select {a} from C,G,GS,S where C.CNo=G.CNo and G.GNo=GS.GNo and GS.SNo=S.SNo and C.CNo='{b}';".format(
                        a=_buf_col,
                        b=MainWindow.UserStatus.User_info
                    )
                elif table_name == "D":
                    _buf_col = "D.DNo,D.CNo,D.Dpay,DPay_yn,DS_yn,DM_yn,S.SNo,S.SName,DS.DSNum,S.SKind,S.SPrice,S.SInventory"
                    SQL_Sentence = "select {a} from D,DS,S where D.CNo='{b}' and D.DNo=DS.DNo and DS.SNo=S.SNo;".format(
                        a=_buf_col,
                        b=MainWindow.UserStatus.User_info
                    )
                elif table_name == "GG":
                    SQL_Sentence = "select * from GG;"
                elif table_name == "S":
                    SQL_Sentence = "select * from S;"
                data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
                description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
                TableSqlAction.TableViewUpdate(MainWindow, description, data)
                MainWindow.TableStatus.Update(table_name, data, description)
        elif MainWindow.UserStatus.User_mode == "P":
            if MainWindow.UserStatus.User_mode != 'P':
                logging.error("User mode is changed when you clicked. Failed to load")
                QMessageBox.information(MainWindow.Qw,'MSG B',
                            "User mode is changed when you clicked. Failed to load!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            else:
                SQL_Sentence = None
                if table_name == "S":
                    SQL_Sentence = "select * from S;"
                elif table_name == "D":
                    _buf_col_ = "distinct GGD.GGNo,GGD.DNo,D.DNo,S.SName,D.CNo,D.DPay_yn,D.DS_yn,DM_yn,C.CPhone,C.CAddr,C.CName"
                    SQL_Sentence = "select {a} from D,GGD,S,C,DS,GS,G where GGD.DNo=D.DNo and GGD.GGNo='{b}'and S.SNo=DS.SNo and C.CNo=G.CNo and D.CNo=C.CNo and DS.DNo=D.DNo;".format(
                        a=_buf_col_,
                        b=MainWindow.UserStatus.User_info
                    )
                elif table_name == "GG":
                    SQL_Sentence = "select * from GG where GG.GGNo='{a}';".format(a=MainWindow.UserStatus.User_info)
                if SQL_Sentence is not None:
                    data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
                    description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
                    TableSqlAction.TableViewUpdate(MainWindow, description, data)
                    MainWindow.TableStatus.Update(table_name, data, description)
                else:
                    logging.info("can't reach")
                    QMessageBox.information(MainWindow.Qw,'MSG B',
                            "????????????????????????!!!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    @staticmethod
    def TableRightMenuContent(MainWindow, qt_point):
        qt_Modleidx = QtWidgets.QTableView.indexAt(MainWindow.tableView,qt_point)
        # print(qt_Modleidx.row(), qt_Modleidx.column())
        MainWindow.tableView.contextMenu = QMenu(MainWindow.Qw)
        MainWindow.statusbar.showMessage("Choose Table {a}, Row{b}, Col{c}".format(
            a=MainWindow.TableStatus.TableName,
            b=qt_Modleidx.row(),
            c=qt_Modleidx.column()
        ))
        if qt_Modleidx.row() == -1 or qt_Modleidx.column() == -1:
            return
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
            if MainWindow.TableStatus.TableName in ["GG"]:
                pass
            elif MainWindow.TableStatus.TableName == "C":
                MainWindow.actionChange = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionChange.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_Change(MainWindow, qt_Modleidx)
                )
            elif MainWindow.TableStatus.TableName == "S":
                MainWindow.actionAdd2G_one = MainWindow.tableView.contextMenu.addAction(r"????????????????????????")
                MainWindow.actionAdd2G_one.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_Add2G_one(MainWindow, qt_Modleidx)
                )
                MainWindow.actionAdd2G_multi = MainWindow.tableView.contextMenu.addAction(r"????????????????????????")
                MainWindow.actionAdd2G_multi.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_Add2G_multi(MainWindow, qt_Modleidx)
                )
                MainWindow.actionSearchSupportor = MainWindow.tableView.contextMenu.addAction(r"???????????????")
                MainWindow.actionSearchSupportor.triggered.connect(
                    lambda:TableSqlAction.TableViewRightClick_SearchSupportor(MainWindow, qt_Modleidx)
                )
            elif MainWindow.TableStatus.TableName == "G":
                MainWindow.actionDelete_one  = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionDelete_one.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_deleteOne(MainWindow, qt_Modleidx, "SNo")
                )
                MainWindow.actionDelete_all = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionDelete_all.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_deleteMulti(MainWindow, qt_Modleidx, "SNo")
                )
                MainWindow.actionSearchSupportor = MainWindow.tableView.contextMenu.addAction(r"???????????????")
                MainWindow.actionSearchSupportor.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_SearchSupportor(MainWindow, qt_Modleidx)
                )
                MainWindow.actionPush2D = MainWindow.tableView.contextMenu.addAction(r"??????????????????????????????")
                MainWindow.actionPush2D.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_Push2D(MainWindow, qt_Modleidx)
                )
            elif MainWindow.TableStatus.TableName == "D":
                MainWindow.actionDelete_one  = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionDelete_one.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_deleteOne(MainWindow, qt_Modleidx, "SNo")
                )
                MainWindow.actionDelete_all = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionDelete_all.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_deleteMulti(MainWindow, qt_Modleidx, "SNo")
                )
        elif MainWindow.UserStatus.User_mode == "P":
            if MainWindow.TableStatus.TableName in ["C", "S", "GG"]:
                pass
            elif MainWindow.TableStatus.TableName == "D":
                # first we should change into S table belong to P first.
                MainWindow.actionDelete_one = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionDelete_one.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_deleteOne(MainWindow, qt_Modleidx, "DNo")
                )
        elif MainWindow.UserStatus.User_mode == "r":
            if MainWindow.TableStatus.TableName in ["C", "GG", "S"]:
                MainWindow.actionChange = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionChange.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_Change(MainWindow, qt_Modleidx)
                )
            if MainWindow.TableStatus.TableName in ["GG", "C", "S"]:
                MainWindow.actionDelete_one = MainWindow.tableView.contextMenu.addAction(r"????????????")
                MainWindow.actionDelete_one.triggered.connect(
                    lambda: TableSqlAction.TableViewRightClick_deleteOne(MainWindow, qt_Modleidx, MainWindow.TableStatus.TableName + "No")
                )

        # MainWindow.actionDelete = MainWindow.tableView.contextMenu.addAction(r"????????????")
        # MainWindow.actionDelete.triggered.connect(lambda:TableSqlAction.TableViewRightClick_deleteOne(MainWindow))
        MainWindow.tableView.contextMenu.popup(QCursor.pos())  # Position of menu
        MainWindow.tableView.contextMenu.show()
