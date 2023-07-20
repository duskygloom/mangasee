from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout

from gui.widgets.mangaframe import MangaFrame
from gui.widgets.stylablewidget import StylableWidget
from gui.widgets.loadinglabel import LoadingLabel
from gui.widgets.clicklabel import ClickLabel

class MangaList(StylableWidget):
    '''contains multiple manga frames'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.status_text = ClickLabel(self)
        self.scrollable = QScrollArea(self)
        self.body = StylableWidget(self.scrollable)
        self.body.setObjectName("basewidget")
        self.decorate()

    def decorate(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.status_text)
        self.status_text.hide()
        self.status_text.setFont(QFont("Consolas", 10, 700))
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.scrollable)
        self.setLayout(layout)
        self.scrollable.setWidget(self.body)
        self.scrollable.setWidgetResizable(True)
        self.bodylayout = QVBoxLayout(self.body)
        self.bodylayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.body.setLayout(self.bodylayout)

    def add_widgets(self, indexname_list):
        self.body.findChild(LoadingLabel).deleteLater()
        for i in indexname_list:
            self.bodylayout.addWidget(MangaFrame(i, self.body))

    def clear_frames(self):
        status = self.body.findChild(ClickLabel, "statuslabel")
        if status is not None:
            status.deleteLater()
        for i in self.body.findChildren(MangaFrame):
            i.deleteLater()

    def set_status(self, fn, done: int, total: int):
        self.status_text.setText(f"{done} out of {total}")
        self.status_text.show()
        self.status_text.set_function(fn)
