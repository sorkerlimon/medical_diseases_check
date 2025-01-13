import cv2
import numpy as np
import os
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QComboBox, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from database import DatabaseManager

class ImageProcessingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_image = None
        self.current_image = None
        self.db_manager = DatabaseManager()
        self.setup_ui()
        
        # Create processed_images directory if it doesn't exist
        self.output_dir = "processed_images"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Left panel (Original Image)
        left_panel = QGroupBox("Original Image")
        left_layout = QVBoxLayout(left_panel)
        
        # Load image button
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        left_layout.addWidget(self.load_button)
        
        # Original image display
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setMinimumSize(400, 400)
        self.original_label.setStyleSheet("QLabel { background-color: #f0f0f0; border: 1px solid #cccccc; }")
        left_layout.addWidget(self.original_label)
        
        # Center panel (Controls)
        center_panel = QGroupBox("Processing Controls")
        center_layout = QVBoxLayout(center_panel)
        
        # Database Connection Button
        self.db_connect_button = QPushButton("Connect to Database")
        self.db_connect_button.clicked.connect(self.connect_database)
        self.db_connect_button.setStyleSheet("""
            QPushButton { background-color: #f0f0f0; }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        center_layout.addWidget(self.db_connect_button)

        # Patient Selection
        patient_selection_group = QGroupBox("Patient Selection")
        patient_selection_layout = QVBoxLayout(patient_selection_group)
        
        self.patient_combo = QComboBox()
        self.patient_combo.setEnabled(False)  # Disabled until database is connected
        self.patient_combo.currentIndexChanged.connect(self.on_patient_selected)
        patient_selection_layout.addWidget(self.patient_combo)
        
        center_layout.addWidget(patient_selection_group)
        
        # Processing method selection
        center_layout.addWidget(QLabel("Processing Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Original",
            "Grayscale",
            "Gaussian Blur",
            "Edge Detection",
            "Threshold"
        ])
        self.method_combo.currentTextChanged.connect(self.process_image)
        center_layout.addWidget(self.method_combo)
        
        # Add Save Button
        self.save_button = QPushButton("Save Processed Image")
        self.save_button.clicked.connect(self.save_processed_image)
        self.save_button.setEnabled(False)  # Disable until image is processed
        center_layout.addWidget(self.save_button)
        
        center_layout.addStretch()
        
        # Right panel (Processed Image)
        right_panel = QGroupBox("Processed Image")
        right_layout = QVBoxLayout(right_panel)
        
        # Processed image display
        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_label.setMinimumSize(400, 400)
        self.processed_label.setStyleSheet("QLabel { background-color: #f0f0f0; border: 1px solid #cccccc; }")
        right_layout.addWidget(self.processed_label)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(center_panel)
        main_layout.addWidget(right_panel)

    def connect_database(self):
        """Handle database connection and show appropriate message"""
        if self.db_manager.connect():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Database Connection")
            msg.setText("Successfully connected to database!")
            msg.setInformativeText("Healthcare database is ready to use.")
            msg.exec()
            
            # Update button appearance to show connected state
            self.db_connect_button.setStyleSheet("""
                QPushButton { 
                    background-color: #90EE90; 
                    border: 1px solid #006400;
                }
                QPushButton:hover { 
                    background-color: #98FB98; 
                }
            """)
            self.db_connect_button.setText("Database Connected")
            self.db_connect_button.setEnabled(False)
            
            # Enable and populate patient dropdown
            self.populate_patient_dropdown()
            self.patient_combo.setEnabled(True)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Database Connection Error")
            msg.setText("Failed to connect to database!")
            msg.setInformativeText("Please check if the database file exists and try again.")
            msg.exec()

    def populate_patient_dropdown(self):
        """Populate the patient dropdown with IDs from database"""
        try:
            self.patient_combo.clear()
            self.patient_combo.addItem("Select Patient ID", None)  # Default option
            
            # Get patient IDs and names from database
            self.db_manager.cursor.execute("SELECT patient_id, patient_name FROM patients")
            patients = self.db_manager.cursor.fetchall()
            
            for patient_id, patient_name in patients:
                # Display both ID and name in dropdown
                self.patient_combo.addItem(f"ID: {patient_id} - {patient_name}", patient_id)
                
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Failed to load patient data!")
            msg.setInformativeText(str(e))
            msg.exec()

    def on_patient_selected(self, index):
        """Handle patient selection from dropdown"""
        if index <= 0:  # Skip if default "Select Patient ID" is selected
            return

        patient_id = self.patient_combo.currentData()
        try:
            # Get patient image name from the database
            self.db_manager.cursor.execute("""
                SELECT patient_image 
                FROM patients 
                WHERE patient_id = ?
            """, (patient_id,))
            
            result = self.db_manager.cursor.fetchone()
            print(result)
            if result and result[0]:
                image_name = result[0]  
                current_dir = os.getcwd()  
                alternate_path = os.path.join(current_dir,  'patient_images', image_name) 
                print(alternate_path)

                # Determine the final path
                if os.path.exists(alternate_path):
                    final_path = alternate_path
                else:
                    final_path = None

                # Handle the resolved path
                if final_path:
                    self.original_image = cv2.imread(final_path)
                    self.display_image(self.original_image, self.original_label)
                    self.process_image()
                else:
                    QMessageBox.warning(self, "Warning", f"Patient image file '{image_name}' not found in either directory!")
            else:
                QMessageBox.information(self, "Information", "No image associated with this patient.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient image: {str(e)}")

            
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", 
                                                 "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.original_image = cv2.imread(file_name)
            self.display_image(self.original_image, self.original_label)
            self.process_image()
    
    def process_image(self):
        if self.original_image is None:
            return
            
        method = self.method_combo.currentText()
        
        if method == "Original":
            processed = self.original_image.copy()
        elif method == "Grayscale":
            processed = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        elif method == "Gaussian Blur":
            kernel_size = 15  # Example fixed kernel size
            processed = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
        elif method == "Edge Detection":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            processed = cv2.Canny(gray, 100, 200)  # Fixed thresholds for edge detection
        elif method == "Threshold":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # Fixed threshold value
        
        self.current_image = processed
        self.display_image(processed, self.processed_label)
        self.save_button.setEnabled(True)  # Enable save button after processing
    
    def save_processed_image(self):
        if self.current_image is None:
            return
            
        method = self.method_combo.currentText()
        timestamp = cv2.getTickCount()  # Use as unique identifier
        filename = f"{method.lower().replace(' ', '_')}_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            if len(self.current_image.shape) == 2:  # Grayscale
                cv2.imwrite(filepath, self.current_image)
            else:  # Color
                cv2.imwrite(filepath, self.current_image)
            
            # Show success message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("Image Saved Successfully!")
            msg.setInformativeText(f"Saved as: {filename}\nLocation: {self.output_dir}")
            msg.exec()
            
        except Exception as e:
            # Show error message if save fails
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText("Failed to save image!")
            error_msg.setInformativeText(str(e))
            error_msg.exec()
    
    def display_image(self, image, label):
        if len(image.shape) == 2:  # Grayscale
            height, width = image.shape
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        else:  # Color
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)

    def __del__(self):
        if hasattr(self, 'db_manager'):
            self.db_manager.close()