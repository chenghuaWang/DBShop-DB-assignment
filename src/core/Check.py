"""
@Author:    chenghua.Wang
@file:      src/core/Check.py
@brief:     Check sql sentence correction first.
"""

import os
import re
import sys
sys.path.append(os.path.split(sys.path[0])[0])


def table_exists(con,table_name):
    """
    input:  [string]table_name
            [Obj-sql-con]con
    Use this function to confirm table is exists or not.
    """
    sql = "select * from sys.tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    con.close()
    if table_name in table_list:
        return True
    else:
        return False