from PyQt6.QtGui import QPaintEvent, QPainter
from PyQt6.QtWidgets import QWidget, QStyle, QStyleOption

class StylableWidget(QWidget):
    '''widget which can be properly styled using stylesheets'''
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def paintEvent(self, a0: QPaintEvent):
        # some hocus pocus from the documentation
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        return super().paintEvent(a0)
