from PyQt6.QtCore import QSize, QObject, QRunnable, pyqtSignal, QThreadPool
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtWidgets import QSizePolicy
from gui.widgets.clicklabel import ClickLabel

from gui.widgets.coloredicon import ColoredIcon
from gui.widgets.mangalist import MangaList
from gui.widgets.loadinglabel import LoadingLabel
from scraper.helper import search_manga, get_all_manga
from scraper.get_resources import get_manga_info

class SearchField(QFrame):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName("searchframe")
        self.inputedit = QLineEdit(self)
        self.searchbutton = QPushButton(self)
        self.mangalist: MangaList = parent.mangalist
        self.decorate()

    def decorate(self):
        self.decorateButton()
        self.decorateInput()
        self.setMaximumHeight(50)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.inputedit)
        layout.addWidget(self.searchbutton)
        self.setLayout(layout)

    def decorateButton(self):
        self.searchbutton.setMinimumSize(75, 50)
        self.searchbutton.setIcon(ColoredIcon("assets/search_icon.svg").get_icon())
        self.searchbutton.setIconSize(QSize(30, 30))
        self.searchbutton.clicked.connect(lambda: self.search_function())

    def decorateInput(self):
        self.inputedit.setMinimumHeight(50)
        self.inputedit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.inputedit.setFont(QFont("Consolas", 14, 700))
        self.inputedit.setPlaceholderText("Search")
        self.inputedit.returnPressed.connect(lambda: self.searchbutton.animateClick())

    def search_function(self):
        self.mangalist.clear_frames()
        loading = LoadingLabel(self.mangalist.body)
        self.mangalist.bodylayout.addWidget(loading)
        loading.timer.start(500)
        pool = QThreadPool.globalInstance()
        worker = MetadataDownloader(self.inputedit.text())
        pool.start(worker)
        worker.signals.began.connect(lambda total: self.mangalist.set_status(lambda: worker.set_stop(), 0, total))
        worker.signals.updated.connect(lambda done, total: self.mangalist.set_status(lambda: worker.set_stop(), done, total))
        worker.signals.finished.connect(lambda l: self.mangalist.add_widgets(l))


class WorkerSingnals(QObject):
    began = pyqtSignal(int)
    finished = pyqtSignal(list)
    updated = pyqtSignal(int, int)

class MetadataDownloader(QRunnable):
    def __init__(self, search: str):
        super().__init__()
        self.search = search
        self.stop = False
        self.signals = WorkerSingnals()

    def set_stop(self, value: bool = True):
        self.stop = value

    def run(self):
        namelist = search_manga(self.search)
        total = len(namelist)
        self.signals.began.emit(total)
        for i in range(len(namelist)):
            if self.stop:
                break
            get_manga_info(namelist[i])
            self.signals.updated.emit(i+1, total)
        self.signals.finished.emit(namelist)
