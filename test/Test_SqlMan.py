"""
@Author:    chenghua.Wang
@file:      src/test/Test_SqlMan.py
@brief:     A test driver function for SqlMan.py in src/core/   
"""
import os
import sys
import logging
sys.path.append(os.path.split(sys.path[0])[0])

import src.core.SqlMan as coSql
import src.core.Phaser as coPh
DEBUG = True

logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    assert DEBUG == True
    user_cfg = coPh.PhaserLoginCfg().GetUser(0)
    SMa = coSql.SqlMan(user_cfg)
    SMa.EX("select * from C where CNo='C12345678'")
    """
    if SMa.TableExists("student") == False:
        # ----------------- Test EX ----------------
        SMa.EX(r"create table student(idx char(16) primary key, name char(16) not null);") # IS OK
    else:
        # ----------------- Test EX ----------------
        SMa.EX(r"create table student(idx char(16) primary key, name char(16) not null);") # IS OK
    # ----------------- Test BatchEx -----------
    ROOT_SQLZOO = r"src\SqlZoo" # IS OK
    SMa.BatchEx(ROOT_SQLZOO + "\Test_BatchEx.sql") # IS OK
    # ----------------- Test Search DS ---------
    babab = SMa.Search("select * from student;") # IS OK
    # print(babab.GetRow(-1))
    babab.print()
    """
    
    