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
        __data__ = SqlSearch.SelfDefined_S(SqlConn, Entity_name, Table_name)
        __describtion__ = SqlSearch.Get_Table_description(SqlConn, Entity_name, Table_name)
        return __data__, __describtion__
