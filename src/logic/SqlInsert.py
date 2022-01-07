"""
@Author:    chenghua.Wang
@file:      src/logic/SqlInsert.py
@brief:     SQl Insert support
"""
import logging
logging.getLogger().setLevel(logging.DEBUG)

class SqlInsert:
    @staticmethod
    def EX_I(SqlConn, rhs):
        """
        input:  [SqlMan-class] SqlConn
                [string] rhs
        output: [SqlSearch_DS-class]
        Use basic EX function in SqlConn class.
        However, this function has highest level of all db,
        use it carefully
        """
        return SqlConn.EX(rhs)