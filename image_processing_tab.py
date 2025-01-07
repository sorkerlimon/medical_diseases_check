from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QLabel, QComboBox, QSlider, QFileDialog, QGraphicsView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np

class ImageProcessingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_image = None
        self.processed_image = None
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        # Left panel for original image
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        left_layout.addWidget(self.load_button)
        self.original_label = QLabel("Original Image")
        left_layout.addWidget(self.original_label)

        # Right panel for processed image
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Controls dropdown menu
        controls_group = QWidget()
        controls_layout = QVBoxLayout(controls_group)
        
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Select Operation", "Grayscale", "Smoothing/Blurring",  "Edge Detection (Canny)", ])
        self.operation_combo.currentIndexChanged.connect(self.apply_image_processing)
        controls_layout.addWidget(self.operation_combo)
        
        # Thresholding slider
        self.slider_label = QLabel("Threshold:")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(127)
        self.slider.valueChanged.connect(self.apply_threshold)
        controls_layout.addWidget(self.slider_label)
        controls_layout.addWidget(self.slider)
        
        right_layout.addWidget(controls_group)
        self.processed_label = QLabel("Processed Image")
        right_layout.addWidget(self.processed_label)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

    def load_image(self):
        """Open file dialog to load an image."""
        file_dialog = QFileDialog(self)
        image_path, _ = file_dialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")
        
        if image_path:
            self.original_image = cv2.imread(image_path)
            self.display_image(self.original_image, self.original_label)

    def display_image(self, img, label):
        """Displays image on a QLabel widget."""
        if img is not None:
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, _ = rgb_image.shape
            q_img = QImage(rgb_image.data, w, h, 3 * w, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def apply_image_processing(self):
        """Apply the selected image processing operation."""
        if self.original_image is not None:
            selected_operation = self.operation_combo.currentText()

            if selected_operation == "Grayscale":
                self.convert_to_grayscale()
            elif selected_operation == "Gaussian Blur":
                self.apply_blur("Gaussian")
            elif selected_operation == "Median Blur":
                self.apply_blur("Median")
            elif selected_operation == "Edge Detection (Canny)":
                self.edge_detection()
            elif selected_operation == "Thresholding":
                self.apply_threshold()
            else:
                self.processed_image = self.original_image
                self.display_image(self.original_image, self.processed_label)

    def convert_to_grayscale(self):
        """Converts the original image to grayscale and displays it."""
        print("Converting to grayscale...")
        grayscale_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.processed_image = grayscale_img
        self.display_image(grayscale_img, self.processed_label)

    def apply_blur(self, blur_type):
        """Applies selected blur filter."""
        print(f"Applying {blur_type} blur...")
        if blur_type == "Gaussian":
            blurred_img = cv2.GaussianBlur(self.original_image, (5, 5), 0)
        elif blur_type == "Median":
            blurred_img = cv2.medianBlur(self.original_image, 5)
        self.processed_image = blurred_img
        self.display_image(blurred_img, self.processed_label)

    def edge_detection(self):
        """Applies Canny edge detection."""
        print("Applying Canny edge detection...")
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        self.processed_image = edges
        self.display_image(edges, self.processed_label)

    def apply_threshold(self):
        """Applies thresholding using the slider value."""
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        _, thresholded_img = cv2.threshold(gray, self.slider.value(), 255, cv2.THRESH_BINARY)
        self.processed_image = thresholded_img
        self.display_image(thresholded_img, self.processed_label)
