# database.py
import sqlite3
from PyQt6.QtWidgets import QMessageBox
from pathlib import Path

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance
    
    def connect(self):
        try:
            db_path = Path("healthcare.db")
            self.connection = sqlite3.connect(str(db_path))
            self.cursor = self.connection.cursor()
            self.create_tables()
            return True
        except sqlite3.Error as e:
            return False
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                patient_age INTEGER,
                patient_gender TEXT,
                patient_contact TEXT,
                patient_image TEXT,
                patient_status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def __del__(self):
        self.close()
