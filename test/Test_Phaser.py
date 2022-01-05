"""
@Author:    chenghua.Wang
@file:      src/core/Test_Phaser.py
@brief:     A test driver function for Phaser.py in src/core/  
"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])

import src.core.Phaser as coPh
DEBUG = True

if __name__ == "__main__":
    assert DEBUG == True
    PLC = coPh.PhaserLoginCfg()
    data = PLC.GetUser()
    print(data)