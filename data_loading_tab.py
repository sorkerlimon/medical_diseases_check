# data_loading_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QGroupBox, QTableWidget, QTableWidgetItem,
                            QMessageBox)
from database import DatabaseManager
import sqlite3

class DataLoadingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Data source group
        source_group = QGroupBox("Data Source")
        source_layout = QVBoxLayout(source_group)
        
        self.load_csv_btn = QPushButton("Load CSV")
        self.connect_db_btn = QPushButton("Connect to Database")
        self.connect_db_btn.clicked.connect(self.connect_to_database)
        
        source_layout.addWidget(self.load_csv_btn)
        source_layout.addWidget(self.connect_db_btn)
        
        # Database operations group
        db_group = QGroupBox("Database Operations")
        db_layout = QVBoxLayout(db_group)
        
        # Create operation buttons with connections
        self.insert_btn = QPushButton("Insert New Data")
        self.retrieve_btn = QPushButton("Retrieve Data")
        self.update_btn = QPushButton("Update Data")
        self.delete_btn = QPushButton("Delete Data")
        
        self.insert_btn.clicked.connect(self.insert_data)
        self.retrieve_btn.clicked.connect(self.retrieve_data)
        self.update_btn.clicked.connect(self.update_data)
        self.delete_btn.clicked.connect(self.delete_data)
        
        for btn in [self.insert_btn, self.retrieve_btn, self.update_btn, self.delete_btn]:
            db_layout.addWidget(btn)
            btn.setEnabled(False)  # Disabled until database connection
        
        # Table view
        self.table = QTableWidget()
        
        # Add all to main layout
        layout.addWidget(source_group)
        layout.addWidget(db_group)
        layout.addWidget(self.table)
    
    def connect_to_database(self):
        if self.db.connect():
            QMessageBox.information(self, "Success", "Connected to database successfully!")
            for btn in [self.insert_btn, self.retrieve_btn, self.update_btn, self.delete_btn]:
                btn.setEnabled(True)
            self.connect_db_btn.setEnabled(False)
        else:
            QMessageBox.critical(self, "Error", "Failed to connect to database!")
    
    def insert_data(self):
        try:
            # Example of inserting sample data
            self.db.cursor.execute('''
                INSERT INTO patients (name, age, gender)
                VALUES (?, ?, ?)
            ''', ("John Doe", 30, "Male"))
            self.db.connection.commit()
            QMessageBox.information(self, "Success", "Data inserted successfully!")
            self.retrieve_data()  # Refresh the view
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to insert data: {str(e)}")
    
    def retrieve_data(self):
        try:
            self.db.cursor.execute('SELECT * FROM patients')
            data = self.db.cursor.fetchall()
            
            # Get column names
            columns = [description[0] for description in self.db.cursor.description]
            
            # Set up table
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
            
            # Fill table with data
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                    
            self.table.resizeColumnsToContents()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve data: {str(e)}")
    
    def update_data(self):
        # Example update operation
        try:
            self.db.cursor.execute('''
                UPDATE patients 
                SET age = age + 1 
                WHERE id = 1
            ''')
            self.db.connection.commit()
            QMessageBox.information(self, "Success", "Data updated successfully!")
            self.retrieve_data()  # Refresh the view
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to update data: {str(e)}")
    
    def delete_data(self):
        try:
            self.db.cursor.execute('DELETE FROM patients WHERE id = 1')
            self.db.connection.commit()
            QMessageBox.information(self, "Success", "Data deleted successfully!")
            self.retrieve_data()  # Refresh the view
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to delete data: {str(e)}")