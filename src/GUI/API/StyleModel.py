"""
@Author:    chenghua.Wang
@file:      src/GUI/API/StyleModel.py
@brief:     QSS format Phaser and builder
"""

import os
import sys
from qt_material import apply_stylesheet

def style_modeling(App, style_name):
    apply_stylesheet(App, theme=style_name)
