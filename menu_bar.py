# menu_bar.py
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenuBar {
                background-color: #f0f0f0;
                border-bottom: 1px solid #ddd;
                min-height: 25px;
                padding: 2px;
            }
            QMenuBar::item {
                spacing: 5px;
                padding: 3px 10px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #34495e;
                color: white;
            }
            QMenuBar::item:pressed {
                background: #2980b9;
                color: white;
            }
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
                border-radius: 3px;
                min-width: 100px;
            }
            QMenu::item:selected {
                background: #e0e0e0;
            }
            QMenu::separator {
                height: 1px;
                background: #ddd;
                margin: 5px 0px;
            }
        """)
        self.create_menus()
    
    def create_menus(self):
        # File menu
        file_menu = self.addMenu("File")
        file_menu.addAction(QAction("Load Data", self))
        file_menu.addAction(QAction("Save", self))
        file_menu.addSeparator()  # Add separator before Exit
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.parent().close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = self.addMenu("View")
        
        # Help menu
        help_menu = self.addMenu("Help")