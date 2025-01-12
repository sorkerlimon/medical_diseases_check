import cv2
import numpy as np
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QComboBox, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap

class ImageProcessingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_image = None
        self.current_image = None
        self.setup_ui()
    
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
            # Convert percentage to kernel size (odd numbers from 1 to 31)
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
