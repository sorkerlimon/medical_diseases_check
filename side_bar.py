# side_bar.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class SideBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        nav_buttons = [
            "Patient Data Management",
            "Health Data Analysis",
            "Spectrum Analysis",
            "Image Processing",
            "Data Visualization"
        ]
        
        for button_text in nav_buttons:
            button = QPushButton(button_text)
            layout.addWidget(button)
            
        layout.addStretch()