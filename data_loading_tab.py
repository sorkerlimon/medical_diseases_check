# data_loading_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QGroupBox, QTableWidget)

class DataLoadingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Data source group
        source_group = QGroupBox("Data Source")
        source_layout = QVBoxLayout(source_group)
        source_layout.addWidget(QPushButton("Load CSV"))
        source_layout.addWidget(QPushButton("Connect to Database"))
        
        # Database operations group
        db_group = QGroupBox("Database Operations")
        db_layout = QVBoxLayout(db_group)
        for op in ["Insert New Data", "Retrieve Data", "Update Data", "Delete Data"]:
            db_layout.addWidget(QPushButton(op))
        
        # Table view
        table = QTableWidget()
        
        # Add all to main layout
        layout.addWidget(source_group)
        layout.addWidget(db_group)
        layout.addWidget(table)
