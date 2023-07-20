from PyQt6.QtWidgets import QMainWindow

from gui.widgets.basewidget import BaseWidget
from gui.widgets.menubar import MenuBar

class MainWindow(QMainWindow):
    '''Custom main window class'''
    def __init__(self, title: str):
        super().__init__()
        self.decorate(title)
        
    def decorate(self, title: str):
        '''customizes self'''
        self.resize(800, 600)
        self.setWindowTitle(title)
        self.setMenuBar(MenuBar(self))
        self.setCentralWidget(BaseWidget(self, "https://mangasee123.com"))
