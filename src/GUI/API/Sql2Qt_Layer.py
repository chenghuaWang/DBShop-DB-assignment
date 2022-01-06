"""
@Author:    chenghua.Wang
@file:      src/GUI/Sql2Qt_Layer.py
@brief:     A Layer tranform between Sql Logic and Qt Action
"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

from logic.SqlSearch import SqlSearch

class LoginSqlAction:
    @staticmethod
    def GetUserTable(SqlConn, Entity_name, Table_name):
        __data__ = SqlSearch.SelfDefined_S(SqlConn, "*", Table_name, "where CNo='{a}'".format(a=Entity_name))
        __describtion__ = SqlSearch.Get_Table_description(SqlConn, "*", Table_name, "where CNo='{a}'".format(a=Entity_name))
        return __data__, __describtion__


class TreeViewSqlAction:
    @staticmethod
    def TreeViewChanged_S(SqlConn, table_name, UserStatus):
        if table_name == UserStatus.UserTable():
            return LoginSqlAction.GetUserTable(SqlConn, UserStatus.User_info, table_name)
        else:
            TABLE = table_name + "," + UserStatus.UserTable()
            __data__ = SqlSearch.SelfDefined_S(SqlConn, "*", TABLE, "where CNo='{a}'".format(a=UserStatus.User_info))
