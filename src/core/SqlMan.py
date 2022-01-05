"""
@Author:    chenghua.Wang
@file:      src/core/SqlMan.py
@brief:     SqlMan for connect to MSSQL server.
            You should first open TCP/IP server for MSSQL,
            and set Port to 5091(by default).
"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

import pymssql
import logging

import src.core.Check as Check

logging.getLogger().setLevel(logging.WARN)

class SqlMan:
    def __init__(self, Usercfg):
        if "User" in Usercfg:
            logging.error("Usercfg has multiple use. You should choose one")
        else:
            self.NickName = Usercfg["NickName"]
            self.Host = Usercfg["Host"]
            self.ServerName = Usercfg["ServerName"]
            self.port = Usercfg["port"]
            self.UserName = Usercfg["UserName"]
            self.pwd = Usercfg["pwd"]
            self.database = Usercfg["database"]
            self.conn = self.__conn__()

    def __conn__(self):
        conn = pymssql.connect(host=self.Host,
            server=self.ServerName, port=self.port, user=self.UserName, 
            password=self.pwd, database=self.database)
        if conn:
            logging.info("Connect success!")
        else:
            logging.error("Sql connect failed.")
        return conn

    def EX(self, rhs):
        """
        input: [string]rhs,
        rhs is recommend to be a single sql sentence.
        ----------------------------------------------
        WARNING:
        cursor.connection.commit() is slow, you should
        aviod use it often. If you want to execute multiple
        sql command, you should use BatchEx function.
        ----------------------------------------------
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(rhs)
            cursor.connection.commit()
        except:
            logging.error("{a} execute wrong.".format(a=rhs))
        
        cursor.close()

    def Search(self, rhs):
        cursor = self.conn.cursor()
        try:
            cursor.execute(rhs)
            AllRow = cursor.fetchall()
            AllRow_DS = SqlSearch_DS(AllRow)
            return AllRow_DS
        except:
            logging.error("{a} execute wrong.".format(a=rhs))
            return SqlSearch_DS(())

    def BatchEx(self, rhs):
        """
        input: [string]rhs, A sql file path.
        exectue sql file
        """
        cursor = self.conn.cursor()
        fd = open(rhs, 'r', encoding='utf-8')
        sqlfile = fd.read()
        fd.close()
        sqlcommamds = sqlfile.split(';')
        for command in sqlcommamds:
            try:
                cursor.execute(command)
            except Exception as msg:
                logging.error("in sql file ex failed execute: {a}".format(a=msg))
        logging.info("sql file ex done.")
        try:
            cursor.connection.commit()
        except:
            logging.warn("commit failed but sql execute is ok")
        cursor.close()

    def TableExists(self, table_name):
        cursor = self.conn.cursor()
        return Check.table_exists(cursor, table_name)


class SqlSearch_DS:
    r"""
    input: [tuple]m_row
    Data struct, for the type returned by DB after search cmd.
    TODO: Tested->false
    """
    def __init__(self, m_row):
        self.m_row = m_row
        self.NumRow = len(self.m_row)
        if self.NumRow == 0:
            self.NumCol = 0
        else:
            self.NumCol = len(self.m_row[0])
    
    def GetRow(self, idx=-1):
        """
        input: [int]idx, if idx is -1 return all, else return idx-ed data.
        """
        if idx == -1:
            return self.m_row
        else:
            if idx < 0 or idx > self.NumRow:
                logging.error("Indexing err, when get row from search concequence")
                exit(1)
            else:
                return self.m_row[idx]

    def print(self):
        if self.NumRow == 0:
            logging.warn("null. No data in search conce")
        else:
            logging.info("-> Has {a} coonce".format(a=self.NumRow))
            for item in self.m_row:
                logging.info("-> {a}".format(a=item))
