from PyQt6.QtGui import QPainter, QPen, QPixmap, QFont, QColor

from config import theme

class DefaultManga(QPixmap):
    '''default manga picture'''
    def __init__(self):
        super().__init__(100, 100)
        self.draw_content()

    def draw_content(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        if theme == "dark":
            self.fill(QColor("#212121"))
            pen = QPen(QColor("#ffffff"))
            # pen = QPen(QColor("#565656"))
        else:
            self.fill(QColor("#ffffff"))
            pen = QPen(QColor("#212121"))
            # pen = QPen(QColor("#a2b9b9"))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setFont(QFont("Consolas", 12, 700))
        painter.drawText(10, 20, "manga")
        painter.end()
