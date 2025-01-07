# tool_bar.py
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setup_actions()
    
    def setup_actions(self):
        self.addAction(QAction("Load Data", self))
        self.addAction(QAction("Save", self))
        self.addAction(QAction("Settings", self))
