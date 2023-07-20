import os

from PyQt6.QtGui import QIcon

import config

class ColoredIcon:
    '''provides svg icons of different colors'''
    def __init__(self, filepath: str):
        self.filepath = filepath
        if config.theme == "light":
            self.color = "#212121"
        else:
            self.color = "#ddffff"

    def change_color(self):
        '''
            changes the color of icon
            returns the path of the colored icon
        '''
        if not os.path.isfile(self.filepath):
            print(f"Icon file does not exist - {self.filepath}")
        else:
            self.iconpath = os.path.dirname(self.filepath)
            self.iconpath = os.path.join(self.iconpath, config.theme, os.path.basename(self.filepath))
            if os.path.isfile(self.iconpath):
                return self.iconpath
            else:
                with open(self.filepath, "r") as fin:
                    with open(self.iconpath, "w") as fout:
                        fout.write(fin.read().replace("<path ", f"<path fill='{self.color}' "))
                return self.iconpath
            
    def get_icon(self):
        '''returns the icon'''
        self.change_color()
        return QIcon(self.iconpath)
