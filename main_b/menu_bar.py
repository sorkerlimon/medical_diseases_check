# menu_bar.py
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_menus()
    
    def create_menus(self):
        # File menu
        file_menu = self.addMenu("File")
        file_menu.addAction(QAction("Load Data", self))
        file_menu.addAction(QAction("Save", self))
        file_menu.addAction(QAction("Exit", self))
        
        # View menu
        view_menu = self.addMenu("View")
        
        # Help menu
        help_menu = self.addMenu("Help")