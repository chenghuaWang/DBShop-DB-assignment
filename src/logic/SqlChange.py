"""
@Author:    chenghua.Wang
@file:      src/logic/SqlChange.py
@brief:     A basic logic for sql when change data.
"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

class SqlChange:
    @staticmethod
    def EX_C(SqlConn, rhs):
        """
        input:  [SqlMan-class] SqlConn
                [string] rhs
        output: [SqlSearch_DS-class]
        Use basic EX function in SqlConn class.
        However, this function has highest level of all db,
        use it carefully
        """
        SqlConn.EX(rhs)
