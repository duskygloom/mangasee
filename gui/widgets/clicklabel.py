from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QLabel, QWidget

class ClickLabel(QLabel):
    '''Label which does stuffs on being clicked'''
    def __init__(self, parent: QWidget, fn = None):
        '''stuff is the function self does'''
        super().__init__(parent)
        if fn != None:
            self.set_function(fn)

    def set_function(self, fn):
        self.fn = fn
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, ev: QMouseEvent):
        if self.fn != None:
            self.fn()
