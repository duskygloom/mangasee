import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem

from gui.widgets.clicklabel import ClickLabel
from gui.widgets.defaultmanga import DefaultManga
import scraper.info as info
import scraper.metadata as metadata
import scraper.helper as helper

class MangaFrame(QFrame):
    '''a frame containing labels to display a search result'''
    def __init__(self, indexname: str, parent: QWidget = None):
        super().__init__(parent)
        self.setObjectName("mangaframe")
        self.indexname = indexname
        self.decorate()
        self.create_labels()

    def decorate(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setContentsMargins(4, 4, 4, 4)

    def create_labels(self):
        '''creates a icon label for displaying manga image'''
        metafile = f"cache/{self.indexname}/metadata.txt"
        cover, title, link = metadata.get_metadata(metafile)
        if cover == "":
            coverpic = DefaultManga()
        else:
            coverpic = QPixmap(cover)
        if title == "":
            title = helper.get_manga_name(self.indexname)
        if link == "":
            link = info.homepage_url + "/manga/" + self.indexname
        self.cover = QLabel(self)
        coverpic = coverpic.scaled(100, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.cover.setPixmap(coverpic)
        self.cover.setFrameStyle(1)
        self.details = QFrame(self)
        self.details.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        details_layout = QVBoxLayout(self.details)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.title = ClickLabel(self.details, lambda: webbrowser.open(link))
        self.title.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.title.setFont(QFont("Consolas", 14, 700))
        self.title.setText(title)
        details_layout.addWidget(self.title)
        layout = QHBoxLayout(self)
        layout.addWidget(self.cover)
        layout.addSpacerItem(QSpacerItem(6, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        layout.addWidget(self.details)
        self.setLayout(layout)
