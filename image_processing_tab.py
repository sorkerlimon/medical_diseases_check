# image_processing_tab.py
import cv2
import numpy as np
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QComboBox, QSlider, QFileDialog,
                            QSpinBox, QGridLayout)
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
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Original",
            "Grayscale",
            "Gaussian Blur",
            "Edge Detection",
            "Threshold"
        ])
        self.method_combo.currentTextChanged.connect(self.process_image)
        center_layout.addWidget(QLabel("Processing Method:"))
        center_layout.addWidget(self.method_combo)
        
        # Gaussian Blur controls
        blur_group = QGroupBox("Blur Settings")
        blur_layout = QGridLayout(blur_group)
        self.blur_kernel = QSpinBox()
        self.blur_kernel.setRange(1, 31)
        self.blur_kernel.setSingleStep(2)
        self.blur_kernel.setValue(5)
        self.blur_kernel.valueChanged.connect(self.process_image)
        blur_layout.addWidget(QLabel("Kernel Size:"), 0, 0)
        blur_layout.addWidget(self.blur_kernel, 0, 1)
        center_layout.addWidget(blur_group)
        
        # Edge detection controls
        edge_group = QGroupBox("Edge Detection Settings")
        edge_layout = QGridLayout(edge_group)
        self.edge_low = QSpinBox()
        self.edge_low.setRange(0, 255)
        self.edge_low.setValue(50)
        self.edge_high = QSpinBox()
        self.edge_high.setRange(0, 255)
        self.edge_high.setValue(150)
        self.edge_low.valueChanged.connect(self.process_image)
        self.edge_high.valueChanged.connect(self.process_image)
        edge_layout.addWidget(QLabel("Low Threshold:"), 0, 0)
        edge_layout.addWidget(self.edge_low, 0, 1)
        edge_layout.addWidget(QLabel("High Threshold:"), 1, 0)
        edge_layout.addWidget(self.edge_high, 1, 1)
        center_layout.addWidget(edge_group)
        
        # Threshold controls
        threshold_group = QGroupBox("Threshold Settings")
        threshold_layout = QGridLayout(threshold_group)
        self.threshold_value = QSpinBox()
        self.threshold_value.setRange(0, 255)
        self.threshold_value.setValue(127)
        self.threshold_value.valueChanged.connect(self.process_image)
        threshold_layout.addWidget(QLabel("Threshold Value:"), 0, 0)
        threshold_layout.addWidget(self.threshold_value, 0, 1)
        center_layout.addWidget(threshold_group)
        
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
            kernel_size = self.blur_kernel.value()
            if kernel_size % 2 == 0:
                kernel_size += 1
            processed = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
        elif method == "Edge Detection":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            processed = cv2.Canny(gray, self.edge_low.value(), self.edge_high.value())
        elif method == "Threshold":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, processed = cv2.threshold(gray, self.threshold_value.value(), 255, cv2.THRESH_BINARY)
        
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