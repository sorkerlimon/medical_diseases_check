# main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from menu_bar import MenuBar
from status_bar import StatusBar
from side_bar import SideBar
from tab_widget import TabWidget

class HealthcareMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Healthcare Data and Medical Image Processing Tool")
        self.setMinimumSize(1200, 800)
        
        # Set up UI components
        self.setup_ui()
        
    def setup_ui(self):
        # Create menu bar
        self.setMenuBar(MenuBar(self))
        

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Add sidebar
        self.sidebar = SideBar(self)
        main_layout.addWidget(self.sidebar, stretch=1)
        
        # Add tab widget
        self.tab_widget = TabWidget(self)
        main_layout.addWidget(self.tab_widget, stretch=4)
        
        # Create status bar
        self.setStatusBar(StatusBar(self))
    

    def closeEvent(self, event):
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, 
            'Exit Application',
            'Are you sure you want to quit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()