from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget

class SideBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        nav_buttons = [
            "Patient Data Management",
        ]
        
        for button_text in nav_buttons:
            button = QPushButton(button_text)
            if button_text == "Patient Data Management":
                button.clicked.connect(self.open_data_loading)
            layout.addWidget(button)
            
        layout.addStretch()
    
    def open_data_loading(self):
        # Find the tab widget in the parent window
        tab_widget = self.parent.findChild(QTabWidget)
        if tab_widget:
            # Find the index of the "Data Loading" tab
            data_loading_index = -1
            for i in range(tab_widget.count()):
                if tab_widget.tabText(i) == "Data Loading":
                    data_loading_index = i
                    break
            
            if data_loading_index != -1:
                tab_widget.setCurrentIndex(data_loading_index)