from PyQt6.QtWidgets import QMenuBar, QMainWindow

class MenuBar(QMenuBar):
    '''Custom menu bar class'''
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
