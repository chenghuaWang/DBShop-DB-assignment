"""
@Author:    chenghua.Wang
@file:      src/GUI/Sql2Qt_Layer.py
@brief:     A Layer tranform between Sql Logic and Qt Action
"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])
import logging

from PyQt5.QtWidgets import QMessageBox

from logic.SqlSearch import SqlSearch
from GUI.API.TableSqlAction import TableSqlAction

class LoginSqlAction:
    @staticmethod
    def main(MainWindow, UserType, ID):
        """
        input:  [string] UserType
                [string] Entity_name
                [string] [Table_name]
                [MainWindow-class] MainWindow
        All logic of LoginAction reflect to Table
        """
        if UserType == 'C':
            SQL_Sentence = "select * from C where CNo='{a}'".format(a=ID)
            data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
            description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
            TableSqlAction.TableViewUpdate(MainWindow, description, data)
            MainWindow.TableSttus.Update("C", data, description)
        elif UserType == 'P':
            SQL_Sentence = "select * from GG where GGNo='{a}';".format(a=ID)
            data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
            description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
            TableSqlAction.TableViewUpdate(MainWindow, description, data)
            MainWindow.TableSttus.Update("GG", data, description)
        elif UserType == 'r':
            SQL_Sentence = "select * from C;"
            data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
            description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
            TableSqlAction.TableViewUpdate(MainWindow, description, data)
            MainWindow.TableSttus.Update("C", data, description)

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

        pass

    @staticmethod
    def User_is_GG(MainWindow, table_name, UserStatus):
        """
        
        """
        pass

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
            if table_name in ["C", "S", "GG"]:
                SQL_Sentence = "select * from {a};".format(a=table_name)
            elif table_name == "G":
                _buf_col = "G.GNo,G.CNo,S.SNo,S.SName,S.SKind,S.SPrice,S.SInventory,GS.GSNum"
                SQL_Sentence = "select {a} from G,C,GS,S where G.GNo=GS.GNo and GS.SNo=S.SNo and G.CNo=C.CNo;".format(a=_buf_col)
            # SQL_Sentence = "select * from {a};".format(a=table_name)
            data = SqlSearch.SelfDefind_S_direct(MainWindow.SqlConn, SQL_Sentence)
            description = SqlSearch.Get_Table_description_direct(MainWindow.SqlConn, SQL_Sentence)
            TableSqlAction.TableViewUpdate(MainWindow, description, data)
            MainWindow.TableSttus.Update(table_name, data, description)


    @staticmethod
    def TreeViewChanged_S(SqlConn, table_name, UserStatus):
        # TODO
        if table_name == UserStatus.UserTable():
            return LoginSqlAction.GetUserTable(SqlConn, UserStatus.User_info, table_name)
        else:
            TABLE = table_name + "," + UserStatus.UserTable()
            __data__ = SqlSearch.SelfDefined_S(SqlConn, "*", TABLE, "where CNo='{a}'".format(a=UserStatus.User_info))
            __describtion__ = SqlSearch.Get_Table_description(SqlConn, "*", TABLE, "where CNO=")  # TODO
