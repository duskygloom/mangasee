import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QWidget, QLabel, QHBoxLayout
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

from gui.widgets.clicklabel import ClickLabel

class HeadPanel(QFrame):
    '''Head of the window'''
    def __init__(self, parent: QWidget, homepage: str):
        super().__init__(parent)
        self.setObjectName("headpanel")
        self.homepage_url = homepage
        self.decorate()

    def decorate(self):
        '''customizes self'''
        text = QLabel(self)
        text.setFont(QFont("Consolas", 20, 700))
        text.setText("MangaSee")
        homeurl = ClickLabel(self, lambda: webbrowser.open_new(self.homepage_url))
        homeurl.setAlignment(Qt.AlignmentFlag.AlignRight)
        homeurl.setAlignment(Qt.AlignmentFlag.AlignBottom)
        homeurl.setFont(QFont("Consolas", 14))
        homeurl.setText(self.homepage_url)
        layout = QHBoxLayout(self)
        layout.addWidget(text)
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(homeurl)
        self.setLayout(layout)
