"""
@Author:    chenghua.Wang(python), ZX.Liu(sql)
@file:      src/logic/SqlSearch.py
"""

import logging
logging.getLogger().setLevel(logging.DEBUG)

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
    def SelfDefined_S(SqlConn, Entity_name, Table_name, judge_logic):
        """
        input:  [SqlMan-class] SqlConn
                [string] rhs
        output: [SqlSearch_DS-class]
        User can determined to search whitch Entity in Sql Table.
        Example: "select #1 from #2"
        """
        RO = "select #1 from #2 #3;"
        RO = RO.replace("#1", Entity_name)
        RO = RO.replace("#2", Table_name)
        RO = RO.replace('#3', judge_logic)
        print(RO)
        return SqlConn.Search(RO)

    @staticmethod
    def Get_Table_description(SqlConn, Entity_name, Table_name, judge_logic):
        """
        input:  [SqlMan-class] SqlConn
                [string] Table_name
        output: List of string with Table Title.
        """
        res = col = None
        RO = "select #1 from #2 #3;"
        RO = RO.replace("#1", Entity_name)
        RO = RO.replace("#2", Table_name)
        RO = RO.replace('#3', judge_logic)
        cursor = SqlConn.conn.cursor()
        try:
            cursor.execute(RO)
            col = cursor.description
            cursor.connection.commit()
        except:
            logging.error("Wrong in get header title.")
        cursor.close()
        if col is not None:
            res = [item[0] for item in col]
        return res
        