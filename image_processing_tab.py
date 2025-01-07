import cv2
import numpy as np
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QComboBox, QSlider, QFileDialog)
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
        
        # Gaussian Blur controls
        blur_group = QGroupBox("Blur Settings")
        blur_layout = QVBoxLayout(blur_group)
        
        blur_label = QLabel("Kernel Size: 0%")
        self.blur_kernel = QSlider(Qt.Orientation.Horizontal)
        self.blur_kernel.setRange(0, 100)
        self.blur_kernel.setValue(20)  # Default 20%
        self.blur_kernel.valueChanged.connect(
            lambda v: (blur_label.setText(f"Kernel Size: {v}%"), self.process_image()))
        
        blur_layout.addWidget(blur_label)
        blur_layout.addWidget(self.blur_kernel)
        center_layout.addWidget(blur_group)
        
        # Edge detection controls
        edge_group = QGroupBox("Edge Detection Settings")
        edge_layout = QVBoxLayout(edge_group)
        
        edge_low_label = QLabel("Low Threshold: 0%")
        self.edge_low = QSlider(Qt.Orientation.Horizontal)
        self.edge_low.setRange(0, 100)
        self.edge_low.setValue(20)  # Default 20%
        self.edge_low.valueChanged.connect(
            lambda v: (edge_low_label.setText(f"Low Threshold: {v}%"), self.process_image()))
        
        edge_high_label = QLabel("High Threshold: 0%")
        self.edge_high = QSlider(Qt.Orientation.Horizontal)
        self.edge_high.setRange(0, 100)
        self.edge_high.setValue(60)  # Default 60%
        self.edge_high.valueChanged.connect(
            lambda v: (edge_high_label.setText(f"High Threshold: {v}%"), self.process_image()))
        
        edge_layout.addWidget(edge_low_label)
        edge_layout.addWidget(self.edge_low)
        edge_layout.addWidget(edge_high_label)
        edge_layout.addWidget(self.edge_high)
        center_layout.addWidget(edge_group)
        
        # Threshold controls
        threshold_group = QGroupBox("Threshold Settings")
        threshold_layout = QVBoxLayout(threshold_group)
        
        threshold_label = QLabel("Threshold Value: 0%")
        self.threshold_value = QSlider(Qt.Orientation.Horizontal)
        self.threshold_value.setRange(0, 100)
        self.threshold_value.setValue(50)  # Default 50%
        self.threshold_value.valueChanged.connect(
            lambda v: (threshold_label.setText(f"Threshold Value: {v}%"), self.process_image()))
        
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.threshold_value)
        center_layout.addWidget(threshold_group)
        
        # Style the sliders
        slider_style = """
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }

            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #52b788, stop:1 #40916c);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }

            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #52b788, stop:1 #40916c);
                border: 1px solid #777;
                height: 8px;
            }
        """
        
        for slider in [self.blur_kernel, self.edge_low, self.edge_high, self.threshold_value]:
            slider.setStyleSheet(slider_style)
        
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
            kernel_size = int(self.blur_kernel.value() / 100 * 30) * 2 + 1
            processed = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
        elif method == "Edge Detection":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            low = int(self.edge_low.value() / 100 * 255)
            high = int(self.edge_high.value() / 100 * 255)
            processed = cv2.Canny(gray, low, high)
        elif method == "Threshold":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            thresh = int(self.threshold_value.value() / 100 * 255)
            _, processed = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        
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