from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                           QGridLayout, QHBoxLayout, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class FeatureCard(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #F8FAFC;
                border-radius: 12px;
                padding: 15px;
                min-height: 120px;
                min-width: 200px;
            }
            QFrame:hover {
                background-color: #F1F5F9;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1E293B;")
        
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #475569;")
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)

class WelcomeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.db = DatabaseManager()
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area for responsiveness
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add stretch for vertical centering
        content_layout.addStretch()
        
        # Content container
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Welcome header
        welcome_label = QLabel("Welcome to Healthcare Data and\nMedical Image Processing System")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        welcome_label.setStyleSheet("color: #1E293B;")
        welcome_label.setWordWrap(True)
        
        # Description
        desc_label = QLabel(
            "This system provides comprehensive tools for managing patient data, "
            "analyzing health records, and processing medical images."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_font = QFont()
        desc_font.setPointSize(11)
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet("color: #475569;")
        
        # Feature cards grid
        features_grid = QGridLayout()
        features_grid.setSpacing(15)
        
        features = [
            ("Patient Management", "Efficiently manage and organize patient records and medical history"),
            ("Medical Analysis", "Advanced tools for analyzing medical data and generating insights"),
            ("Visual Analytics", "Powerful visualization tools for medical image processing")
        ]
        
        # Responsive grid layout
        def update_grid_layout():
            # Clear existing items
            while features_grid.count():
                item = features_grid.takeAt(0)
                if item.widget():
                    item.widget().hide()
                    features_grid.removeWidget(item.widget())

            # Calculate columns based on width
            width = self.width()
            if width < 600:
                cols = 1
            elif width < 900:
                cols = 2
            else:
                cols = 3

            # Add cards to grid
            for i, (title, desc) in enumerate(features):
                row = i // cols
                col = i % cols
                card = FeatureCard(title, desc)
                features_grid.addWidget(card, row, col)

        # Navigation hint
        nav_hint = QLabel("Please use the tabs above to navigate through different features of the application")
        nav_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_hint.setWordWrap(True)
        nav_hint.setStyleSheet("""
            QLabel {
                background-color: #EFF6FF;
                color: #1E40AF;
                padding: 16px;
                border-radius: 8px;
            }
        """)
        
        # Add all elements to container layout
        container_layout.addWidget(welcome_label)
        container_layout.addWidget(desc_label)
        container_layout.addLayout(features_grid)
        container_layout.addWidget(nav_hint)
        
        # Add container to content layout
        content_layout.addWidget(container)
        
        # Add bottom stretch for vertical centering
        content_layout.addStretch()
        
        # Set content widget in scroll area
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
        
        # Set background color for the entire tab
        self.setStyleSheet("background-color: #F8FAFC;")
        
        # Set minimum size
        self.setMinimumSize(300, 400)
        
        # Initial grid layout
        update_grid_layout()
        
        # Store update_grid_layout for resize events
        self._update_grid_layout = update_grid_layout

    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        # Update grid layout when window is resized
        self._update_grid_layout()
        
        # Adjust font sizes based on window width
        width = event.size().width()
        welcome_font_size = max(14, min(16, width // 50))
        desc_font_size = max(10, min(11, width // 60))
        
        # Update welcome label font
        for label in self.findChildren(QLabel):
            if "Welcome" in label.text():
                font = label.font()
                font.setPointSize(welcome_font_size)
                label.setFont(font)
            elif "This system provides" in label.text():
                font = label.font()
                font.setPointSize(desc_font_size)
                label.setFont(font)