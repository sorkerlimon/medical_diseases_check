# image_processing_tab.py
import cv2
import numpy as np
import os
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QComboBox, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from aimodel import BrainMRIClassifier
import tempfile
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
        self.patient_combo.setEnabled(False)
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
        self.save_button.setEnabled(False)
        center_layout.addWidget(self.save_button)

        # Add Prediction Button
        self.prediction_button = QPushButton("Prediction")
        self.prediction_button.clicked.connect(self.perform_prediction)
        # self.prediction_button.setEnabled(False)  # Enable when processing is done
        center_layout.addWidget(self.prediction_button)

        # Add Status Display Group Box
        status_group = QGroupBox("Processing Status")
        status_layout = QVBoxLayout(status_group)

        # Add status labels
        self.image_size_label = QLabel("Image Size: -")
        self.processing_method_label = QLabel("Current Method: -")
        self.pixel_range_label = QLabel("Pixel Range: -")
        self.mean_intensity_label = QLabel("Mean Intensity: -")

        status_layout.addWidget(self.image_size_label)
        status_layout.addWidget(self.processing_method_label)
        status_layout.addWidget(self.pixel_range_label)
        status_layout.addWidget(self.mean_intensity_label)

        center_layout.addWidget(status_group)
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

    def perform_prediction(self):
        """Perform prediction on the original image."""
        if self.original_image is None:
            QMessageBox.warning(self, "Warning", "No original image available for prediction!")
            return

        try:
            # Save the NumPy array as a temporary image file
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                temp_image_path = temp_file.name
                cv2.imwrite(temp_image_path, self.original_image)

            # Initialize the BrainMRIClassifier
            model_path = 'model_weights_vgg.keras'  # Update with the path to your model
            classifier = BrainMRIClassifier(model_path)

            # Perform prediction
            predictions = classifier.predict_image(temp_image_path)

            # Display results in a message box and generate a detailed report
            report = classifier.generate_report(predictions)
            predicted_class = report['predicted_class']
            confidence = report['confidence']

            QMessageBox.information(
                self,
                "Prediction Result",
                f"Predicted Class: {predicted_class}\n"
                f"Confidence: {confidence:.2f}%\n\n"
                f"Detailed Probabilities:\n" +
                "\n".join([f"{class_name}: {prob:.2f}%" for class_name, prob in report['class_probabilities'].items()])
            )

            # Plot the results
            # classifier.plot_results(predictions)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to perform prediction: {str(e)}")

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
            if result and result[0]:
                image_name = result[0]
                current_dir = os.getcwd()
                alternate_path = os.path.join(current_dir, 'patient_images', image_name)

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
                    QMessageBox.warning(self, "Warning", f"Patient image file '{image_name}' not found!")
            else:
                QMessageBox.information(self, "Information", "No image associated with this patient.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient image: {str(e)}")

    def load_image(self):
        """Load image from file system"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.original_image = cv2.imread(file_name)
            self.display_image(self.original_image, self.original_label)
            self.process_image()
            
    
    def update_status_info(self):
        """Update the status information labels with current image details"""
        if self.current_image is None:
            return
            
        # Update image size
        if len(self.current_image.shape) == 3:
            height, width, channels = self.current_image.shape
            self.image_size_label.setText(f"Image Size: {width}x{height}x{channels}")
        else:
            height, width = self.current_image.shape
            self.image_size_label.setText(f"Image Size: {width}x{height}")
            
        # Update processing method
        current_method = self.method_combo.currentText()
        self.processing_method_label.setText(f"Current Method: {current_method}")
        
        # Update pixel range
        min_val = np.min(self.current_image)
        max_val = np.max(self.current_image)
        self.pixel_range_label.setText(f"Pixel Range: {min_val} - {max_val}")
        
        # Update mean intensity
        mean_val = np.mean(self.current_image)
        self.mean_intensity_label.setText(f"Mean Intensity: {mean_val:.2f}")
    
    def process_image(self):
        """Process the image using selected method"""
        if self.original_image is None:
            return
            
        method = self.method_combo.currentText()
        
        if method == "Original":
            processed = self.original_image.copy()
        elif method == "Grayscale":
            processed = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        elif method == "Gaussian Blur":
            kernel_size = 15
            processed = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
        elif method == "Edge Detection":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            processed = cv2.Canny(gray, 100, 200)
        elif method == "Threshold":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        self.current_image = processed
        self.display_image(processed, self.processed_label)
        self.save_button.setEnabled(True)
        
        # Update status information after processing
        self.update_status_info()
    
    def save_processed_image(self):
        """Save the processed image to file system"""
        if self.current_image is None:
            return
            
        method = self.method_combo.currentText()
        timestamp = cv2.getTickCount()
        filename = f"{method.lower().replace(' ', '_')}_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            cv2.imwrite(filepath, self.current_image)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("Image Saved Successfully!")
            msg.setInformativeText(f"Saved as: {filename}\nLocation: {self.output_dir}")
            msg.exec()
            
        except Exception as e:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText("Failed to save image!")
            error_msg.setInformativeText(str(e))
            error_msg.exec()
    
    def display_image(self, image, label):
        """Display the image in the provided label"""
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
        """Clean up database connection on deletion"""
        if hasattr(self, 'db_manager'):
            self.db_manager.close()