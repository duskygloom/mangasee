from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget, QLabel

import config

class LoadingLabel(QLabel):
    '''pixmap but contains loading pictures'''
    def __init__(self, parent: QWidget = None, maxdots: int = 3):
        super().__init__(parent)
        self.setObjectName("loadinglabel")
        self.maxdots = maxdots
        self.curdots = 0
        self.decorate()
        self.decorate_canvas()
        
    def decorate(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def decorate_canvas(self):
        self.canvas = QPixmap(63*self.maxdots, 60)          # 60+3 to accomodate the brush thickness
        self.canvas.fill(QColor(0, 0, 0, 0))
        self.setPixmap(self.canvas)
        if config.theme == "dark":
            self.pen = QPen(QColor("#565656"))
        elif config.theme == "light":
            self.pen = QPen(QColor("#a2b9b9"))
        self.pen.setWidth(3)
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.increase_dots())

    def increase_dots(self):
        if self.curdots < self.maxdots:
            self.curdots += 1
        else:
            self.curdots = 0
        self.draw_dots(self.curdots)
    
    def draw_dots(self, n: int):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        self.canvas.fill(QColor(0, 0, 0, 0))
        for i in range(n):
            painter.drawEllipse(30+(60*i), 30, 12, 12)
        painter.end()
        self.setPixmap(self.canvas)
