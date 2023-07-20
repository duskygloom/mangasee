from PyQt6.QtWidgets import QVBoxLayout, QMainWindow

from gui.widgets.headpanel import HeadPanel
from gui.widgets.searchfield import SearchField
from gui.widgets.mangalist import MangaList
from gui.widgets.stylablewidget import StylableWidget

class BaseWidget(StylableWidget):
    '''custom base widget class'''
    def __init__(self, parent: QMainWindow, homepage: str):
        super().__init__(parent)
        self.setObjectName("basewidget")
        self.homepage_url = homepage
        self.decorate()

    def decorate(self):
        '''customizes self'''
        self.mangalist = MangaList(self)
        layout = QVBoxLayout(self)
        layout.addWidget(HeadPanel(self, self.homepage_url))
        layout.addWidget(SearchField(self))
        layout.addWidget(self.mangalist)
        self.setLayout(layout)
