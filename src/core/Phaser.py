"""
@Author:    chenghua.Wang
@file:      src/core/Phaser.py
@brief:     Basic Phaser for json-like config.   
"""

import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

import json
import logging
logging.getLogger().setLevel(logging.WARN)


class PhaserLoginCfg:
    """
    Phaser Login cfg from config folder.
    Only readable, you can not use this class to rewrite.
    """
    def __init__(self, cfg_path=r"src\config\LoginCfg.json"):
        self.cfg_path = cfg_path
        with open(self.cfg_path,'r',encoding='utf8')as fp:
            self.data = json.load(fp)
    
    def GetRawData(self):
        """
        return [dictionary]self.data,
        self.data havs ond only has "User" and "Manager" key.
        """
        return self.data

    def GetUser(self, idx=-1):
        """
        input:  [int]idx, idx default is -1, which means return all cfg.
        return: AllUser when idx is -1, else return the idx user.
        """
        if idx == -1:
            return self.data["User"]
        else:
            len_buf = len(self.data["User"])
            if idx > len_buf:
                logging.error("Out of range.")
                exit(1)
            else:
                return self.data["User"][idx]

    def GetManager(self, idx=-1):
        """
        Same as [function] GetUser.
        input:  [int]idx, idx default is -1, which means return all cfg.
        return: AllUser when idx is -1, else return the idx user.
        """
        if idx == -1:
            return self.data["Manager"]
        else:
            len_buf = len(self.data["Manager"])
            if idx > len_buf:
                logging.error("Out of range.")
                exit(1)
            else:
                return self.data["Manager"][idx]


class PhaserCfg:
    def __init__(self, cfg_path=r"src\config\GlobalCfg.json"):
        pass

