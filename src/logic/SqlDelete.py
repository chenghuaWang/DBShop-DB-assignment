"""
@Author:    chenghua.Wang
@file:      src/logic/SqlDelete.py
@brief:     SQl Delete support
"""
import logging
logging.getLogger().setLevel(logging.DEBUG)

class SqlDelete:
    @staticmethod
    def EX_D(SqlConn, rhs):
        """
        input:  [SqlMan-class] SqlConn
                [string] rhs
        output: [SqlSearch_DS-class]
        Use basic EX function in SqlConn class.
        However, this function has highest level of all db,
        use it carefully
        """
        return SqlConn.EX(rhs)
    