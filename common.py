import sys
import os
import platform

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path =  sys._MEIPASS       # x86

        if platform.system() != 'Windows':
            base_path =  '/home/emws/'    # linux
            
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)