"""
@Author:    chenghua.Wang
@file:      src/GUI/Sql2Qt_Layer.py
@brief:     A Layer tranform between Sql Logic and Qt Action
"""
import os
import sys
import logging
import hashlib

from src.core.SqlMan import SqlMan
from src.logic.SqlChange import SqlChange
sys.path.append(os.path.split(sys.path[0])[0])


from PyQt5.QtWidgets import QMessageBox

from logic.SqlSearch import SqlSearch
from GUI.API.TableSqlAction import TableSqlAction
from GUI.API.login_register_window import Login_Register_Window
from core.Phaser import PhaserLoginCfg

class LoginSqlAction:
    @staticmethod
    def main(MainWindow, UserType, ID, Pwd):
        """
        input:  [string] UserType
                [string] Entity_name
                [string] [Table_name]
                [MainWindow-class] MainWindow
        All logic of LoginAction reflect to Table
        """
        if LoginSqlAction.ComparePwd(MainWindow, UserType, ID, Pwd):
            if UserType == 'C':
                SQL_Sentence = "select * from C where CNo='{a}'".format(a=ID)
                data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
                description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
                TableSqlAction.TableViewUpdate(MainWindow, description, data)
                MainWindow.TableStatus.Update("C", data, description)
            elif UserType == 'P':
                SQL_Sentence = "select * from GG where GGNo='{a}';".format(a=ID)
                data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
                description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
                TableSqlAction.TableViewUpdate(MainWindow, description, data)
                MainWindow.TableStatus.Update("GG", data, description)
            elif UserType == 'r':
                SQL_Sentence = "select * from C;"
                data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
                description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
                TableSqlAction.TableViewUpdate(MainWindow, description, data)
                MainWindow.TableStatus.Update("C", data, description)
        else:
            logging.error("User {a} Not exits, or Pwd wrong".format(a=ID))
            QMessageBox.information(MainWindow.Qw,'Error',
                        "User {a} Not exits, or Pwd wrong".format(a=ID),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    @staticmethod
    def LoginWindow_TableViewChange(MainWindow, ID, TableName):
        data, describe = LoginSqlAction.GetUserTable(MainWindow.SqlConn, ID, TableName)
        TableSqlAction.TableViewUpdate(MainWindow, describe, data)
        # self.TableViewUpdate(describe, data)

    @staticmethod
    def GetUserTable(SqlConn, Entity_name, Table_name):
        """
        A Test function, only used in main->Usertype=C,
        in other case, use SqlSearch pac directly
        """
        __data__ = SqlSearch.SelfDefined_S(SqlConn, "*", Table_name, "where CNo='{a}'".format(a=Entity_name))
        __describtion__ = SqlSearch.Get_Table_description(SqlConn, "*", Table_name, "where CNo='{a}'".format(a=Entity_name))
        return __data__, __describtion__

    @staticmethod
    def ComparePwd(MainWindow, UserType, UserID, pwd):
        if UserType == "r":
            PL = PhaserLoginCfg()
            ori_id = PL.GetManager(0)["ManagerName"]
            ori_pwd = PL.GetManager(0)["Password"]
            if UserID == ori_id and hashlib.md5(pwd.encode("utf8")).hexdigest() == ori_pwd:
                return True
            else:
                return False
        elif UserType == "C":
            sql = " "
            ori_pwd = None
            sql = "select CMNo from CM where CNo='{a}';".format(a=UserID)
            ori_pwd = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, sql)
            if ori_pwd == None or ori_pwd.NumRow_f() == 0:
                return False
            else:
                ori_pwd = ori_pwd.m_row[0][0][0:-1]
                if hashlib.md5(pwd.encode("utf8")).hexdigest() == ori_pwd:
                    return True
                else:
                    return False
        elif UserType == "P":
            sql = " "
            ori_pwd = None
            sql = "select GGMNo from GGM where GGNo='{a}';".format(a=UserID)
            ori_pwd = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, sql)
            if ori_pwd == None or ori_pwd.NumRow_f() == 0:
                return False
            else:
                ori_pwd = ori_pwd.m_row[0][0][0:-1]
                if hashlib.md5(pwd.encode("utf8")).hexdigest() == ori_pwd:
                    return True
                else:
                    return False


class TreeViewSqlAction:
    """
    In this block, implement click event in TreeView.
    """
    @staticmethod
    def getTableName(QModelidx):
        if QModelidx.row() == 0:
            table_name = "C"
        elif QModelidx.row() == 1:
            table_name = "S"
        elif QModelidx.row() == 2:
            table_name = "G"
        elif QModelidx.row() == 3:
            table_name = "GG"
        elif QModelidx.row() == 4:
            table_name = "D"
        return table_name

    @staticmethod
    def main(MainWindow, QModelidx):
        table_name = TreeViewSqlAction.getTableName(QModelidx)
        if MainWindow.UserStatus.User_mode == "r":
            TreeViewSqlAction.User_is_root(MainWindow, table_name, MainWindow.UserStatus)
        elif MainWindow.UserStatus.User_mode == "C":
            TreeViewSqlAction.User_is_C(MainWindow, table_name, MainWindow.UserStatus)
        elif MainWindow.UserStatus.User_mode == "P":
            TreeViewSqlAction.User_is_GG(MainWindow, table_name, MainWindow.UserStatus)
        
    @staticmethod
    def User_is_C(MainWindow, table_name, UserStatus):
        """
        Logic, When User is C. The Logic of TreeView.
        1. When Click Table C -> 
        2. When Click Table S -> User can chose which added into G.
        3. When Click Table G -> User can delete item from G. User can use right click to get in GG table.
        4. When Click Table GG -> User can check info in S.
        WARNNING:
        This function need to return A status wether other Action in MainWindow need be execute.
        """
        if UserStatus.User_mode != 'C':
            logging.error("User mode is changed when you clicked. Failed to load")
            QMessageBox.information(MainWindow.Qw,'MSG B',
                        "User mode is changed when you clicked. Failed to load!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        else:
            if table_name == "C":
                SQL_Sentence = "select * from C where CNo='{a}';".format(a=UserStatus.User_info)
            elif table_name == "G":
                _buf_col = "G.GNo,C.CNo,S.SNo,S.SName,S.SKind,S.SPrice,S.SInventory,GS.GSNum"
                SQL_Sentence = "select {a} from C,G,GS,S where C.CNo=G.CNo and G.GNo=GS.GNo and GS.SNo=S.SNo and C.CNo='{b}';".format(
                    a=_buf_col,
                    b=UserStatus.User_info
                )
            elif table_name == "D":
                _buf_col = "D.DNo,D.CNo,D.Dpay,DPay_yn,DS_yn,DM_yn,S.SNo,S.SName,DS.DSNum,S.SKind,S.SPrice,S.SInventory"
                SQL_Sentence = "select {a} from D,DS,S where D.CNo='{b}' and D.DNo=DS.DNo and DS.SNo=S.SNo;".format(
                    a=_buf_col,
                    b=UserStatus.User_info
                )
            elif table_name == "GG":
                SQL_Sentence = "select * from GG;"
            elif table_name == "S":
                SQL_Sentence = "select * from S;"
            data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
            description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
            TableSqlAction.TableViewUpdate(MainWindow, description, data)
            MainWindow.TableStatus.Update(table_name, data, description)
           
    @staticmethod
    def User_is_GG(MainWindow, table_name, UserStatus):
        """
        GG is the supporter of S.
        They can not see G Table Custom Table.
        Thay are aable to access in to S, GG, D Table
        """
        if UserStatus.User_mode != 'P':
            logging.error("User mode is changed when you clicked. Failed to load")
            QMessageBox.information(MainWindow.Qw,'MSG B',
                        "User mode is changed when you clicked. Failed to load!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        else:
            SQL_Sentence = None
            if table_name == "S":
                SQL_Sentence = "select * from S;"
            elif table_name == "D":
                _buf_col_ = "distinct GGD.GGNo,GGD.DNo,S.SName,D.CNo,D.DPay_yn,D.DS_yn,DM_yn,C.CPhone,C.CAddr,C.CName"
                SQL_Sentence = "select {a} from D,GGD,S,C,DS,GS,G where GGD.DNo=D.DNo and GGD.GGNo='{b}'and S.SNo=DS.SNo and C.CNo=G.CNo and D.CNo=C.CNo and DS.DNo=D.DNo;".format(
                    a=_buf_col_,
                    b=UserStatus.User_info
                )
            elif table_name == "GG":
                _buf_ = "GG.GGNo,GG.GGName,GG.GGAddr,S.SNo,S.SName,S.SKind,S.SPrice,S.SInventory"
                SQL_Sentence = "select {cho} from GG,S,GGS where GG.GGNo='{a}' and GG.GGNo=GGS.GGNo and S.SNo=GGS.SNo;".format(
                    cho=_buf_,
                    a=UserStatus.User_info
                )
            if SQL_Sentence is not None:
                data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
                description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
                TableSqlAction.TableViewUpdate(MainWindow, description, data)
                MainWindow.TableStatus.Update(table_name, data, description)
            else:
                logging.info("can't reach")
                QMessageBox.information(MainWindow.Qw,'MSG B',
                        "你不能查看这张表!!!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    @staticmethod
    def User_is_root(MainWindow, table_name, UserStatus):
        """
        Show Every Table To User-root
        """
        if UserStatus.User_mode != "r":
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


class MenuInsertSqlAction:
    @staticmethod
    def main(MainWindow):
        """
        "P" can insert to "S"
        "r" can insert to "all"
        """
        if MainWindow.UserStatus.User_mode in ["P", "r"]:
            if MainWindow.UserStatus.User_mode == "P" and MainWindow.TableStatus.TableName == "S":
                MainWindow.Insert_childWindow.initData()
                MainWindow.Insert_childWindow.show()
            elif MainWindow.UserStatus.User_mode == "r":
                MainWindow.Insert_childWindow.initData()
                MainWindow.Insert_childWindow.show()
            else:
                QMessageBox.information(MainWindow.Qw,'MSG B',
                        "商户只能增加S表的信息!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        else:
            QMessageBox.information(MainWindow.Qw,'MSG B',
                        "客户不能直接插入数据!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)


class LineEditSqlAction:
    @staticmethod
    def main(MainWindow):
        text_buf = MainWindow.lineEdit.text()
        MainWindow.lineEdit.setText("")
        LineEditSqlAction.Exc(MainWindow, LineEditSqlAction.Phaser(text_buf))

    @staticmethod
    def Phaser(rhs):
        """
        sql:select * from ...
        sql_search:select...
        info:Version
        """
        return rhs.split(":")

    @staticmethod
    def Exc(MainWindow, rhs_list):
        if rhs_list[0] == "sql":
            SqlChange.EX_C(MainWindow.SqlConn, rhs_list[1])
            MainWindow.statusbar.showMessage("sql->{a}".format(a=rhs_list[1]), 2*1000)
        elif rhs_list[0] == "info":
            if rhs_list[1] == "Version":
                MainWindow.statusbar.showMessage("info->Vision. 0.0.6 beta", 10*1000)
        elif rhs_list[0] == "sql_search":
            try:
                _data_ = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, rhs_list[1])
                _describe_ = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, rhs_list[1])
                MainWindow.SearchTable_childWindow.UpdateTableData(TableSqlAction, _data_, _describe_)
                MainWindow.SearchTable_childWindow.show()
            except:
                logging.error("Sql sentence wrong in lineEdit!")
                QMessageBox.information(MainWindow.Qw,'ERROR',
                        "Sql sentence wrong in lineEdit!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)


class SelectSqlAction:
    @staticmethod
    def main(MainWindow):
        if MainWindow.TableStatus.TableName in ["S","D","C","GG","G"]:
            MainWindow.Select_childWindow.updateSelectBar(MainWindow.TableStatus.describe)
            MainWindow.Select_childWindow.show()


class LoginSqlAction_new:
    @staticmethod
    def main(MainWindow):
        MainWindow.Login_Register_childWindow.SetWindowMode("Login")
        MainWindow.Login_Register_childWindow.SetALLLLTextClear()
        MainWindow.Login_Register_childWindow.show()


class RegisterSqlAction:
    @staticmethod
    def main(MainWindow, TableName):
        MainWindow.Login_Register_childWindow.SetWindowMode("Register")
        MainWindow.Login_Register_childWindow.SetALLLLTextClear()
        MainWindow.Login_Register_childWindow.show()
