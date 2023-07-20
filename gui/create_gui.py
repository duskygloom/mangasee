import sys, os, shutil

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

import config
from gui.widgets.mainwindow import MainWindow
from scraper.get_resources import get_mangasee_icon

stylesheet_file = "gui/" + config.theme + "_stylesheet.qss"

def create_gui(arguments: list[str]):
    '''creates the gui for the manga downloader'''
    app = QApplication(arguments)
    iconpath = get_mangasee_icon()
    app.setWindowIcon(QIcon(iconpath))
    if os.path.isfile(stylesheet_file):
        with open(stylesheet_file, "r") as f:
            app.setStyleSheet(f.read())
    win = MainWindow("Mangasee Downloader")
    win.show()
    app.exec()
    cachedir = "cache"
    dirsize = 0
    for dirname, dirs, files in os.walk(cachedir):
        for f in files:
            dirsize += os.path.getsize(os.path.join(dirname, f))
    if dirsize > 100000000:
        shutil.rmtree(cachedir)
        os.mkdir(cachedir)
    sys.exit()
