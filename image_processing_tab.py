# image_processing_tab.py
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                            QLabel, QGroupBox, QComboBox, QSlider)
from PyQt6.QtCore import Qt

class ImageProcessingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QPushButton("Load Image"))
        left_layout.addWidget(QLabel("Original Image"))
        
        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Controls
        controls_group = QGroupBox("Image Processing")
        controls_layout = QVBoxLayout(controls_group)
        
        controls_layout.addWidget(QPushButton("Convert to Grayscale"))
        
        blur_combo = QComboBox()
        blur_combo.addItems(["Gaussian Blur", "Median Blur"])
        controls_layout.addWidget(blur_combo)
        
        controls_layout.addWidget(QPushButton("Edge Detection"))
        controls_layout.addWidget(QLabel("Threshold:"))
        controls_layout.addWidget(QSlider(Qt.Orientation.Horizontal))
        
        right_layout.addWidget(controls_group)
        right_layout.addWidget(QLabel("Processed Image"))
        
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)