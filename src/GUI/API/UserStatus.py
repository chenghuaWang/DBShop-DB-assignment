"""
@Author:    chenghua.Wang
@file:      src/GUI/UserStatus.py
@brief:     UserStatus. Judge in Qt MainWindow
"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

class UserStatus_DS:
    def __init__(self, User_mode, User_info):
        self.User_mode = User_mode
        self.User_info = User_info

    def Update(self, User_mode, User_info):
        self.User_info = User_info
        self.User_mode = User_mode

    def UserTable(self):
        if self.User_mode == "P":
            return "GG"
        elif self.User_mode == "C":
            return "C"
        elif self.User_mode == "r":
            return "r"