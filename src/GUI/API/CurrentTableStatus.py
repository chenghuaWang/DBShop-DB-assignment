"""
@Author:    chenghua.Wang
@file:      src/GUI/CurrentTableStatus.py
@brief:     Load and store current TableView is showing witch table in sql.
"""
class CurrentTableStatus:
    def __init__(self, TableName):
        self.TableName = TableName

    def Update(self, TableName, data, describe):
        self.TableName = TableName
        self.data = data
        self.describe = describe
        self.Row = len(self.describe)
        if self.Row == 0:
            self.Col = 0
        else:
            self.Col = len(self.describe[0])