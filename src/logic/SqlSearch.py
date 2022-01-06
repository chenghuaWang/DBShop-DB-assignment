"""
@Author:    chenghua.Wang(python), ZX.Liu(sql)
@file:      src/logic/SqlSearch.py
"""

import logging
logging.getLogger().setLevel(logging.INFO)

class SqlSearch:
    @staticmethod
    def EX_S(SqlConn, rhs):
        """
        input:  [SqlMan-class] SqlConn
                [string] rhs
        output: [SqlSearch_DS-class]
        Use basic EX function in SqlConn class.
        However, this function has highest level of all db,
        use it carefully
        """
        return SqlConn.EX(rhs)

    @staticmethod
    def SelfDefined_S(SqlConn, Entity_name, Table_name):
        """
        input:  [SqlMan-class] SqlConn
                [string] rhs
        output: [SqlSearch_DS-class]
        User can determined to search whitch Entity in Sql Table.
        Example: "select #1 from #2"
        """
        RO = "select #1 from #2"
        RO = RO.replace("#1", Entity_name)
        RO = RO.replace("#2", Table_name)
        return SqlConn.EX(RO)

    @staticmethod
    def Get_Table_description(SqlConn, Entity_name, Table_name):
        """
        input:  [SqlMan-class] SqlConn
                [string] Table_name
        output: List of string with Table Title.
        """
        RO = "select #1 from #2"
        RO = RO.replace("#1", Entity_name)
        RO = RO.replace("#2", Table_name)
        cursor = SqlConn.conn.cursor()
        try:
            cursor.excute(RO)
            col = cursor.description
            cursor.connection.commit()
        except:
            logging.error("Wrong in get header title.")
        cursor.close()
