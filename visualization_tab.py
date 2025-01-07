# visualization_tab.py
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                            QComboBox, QPushButton, QLabel, QSlider, QScrollArea)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import seaborn as sns

class VisualizationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Left Panel - Controls
        controls_panel = QWidget()
        controls_layout = QVBoxLayout(controls_panel)
        
        # Chart Type Selection
        chart_group = QGroupBox("Chart Type")
        chart_layout = QVBoxLayout(chart_group)
        
        self.chart_combo = QComboBox()
        self.chart_combo.addItems([
            "Time Series Plot",
            "Scatter Plot",
            "Heatmap",
            "FFT Plot"
        ])
        self.chart_combo.currentTextChanged.connect(self.update_visualization)
        chart_layout.addWidget(self.chart_combo)
        controls_layout.addWidget(chart_group)
        
        # Data Selection
        data_group = QGroupBox("Data Selection")
        data_layout = QVBoxLayout(data_group)
        
        # X-axis data
        data_layout.addWidget(QLabel("X-Axis Data:"))
        self.x_combo = QComboBox()
        self.x_combo.addItems(["Time", "Heart Rate", "Blood Pressure", "Temperature"])
        self.x_combo.currentTextChanged.connect(self.update_visualization)
        data_layout.addWidget(self.x_combo)
        
        # Y-axis data
        data_layout.addWidget(QLabel("Y-Axis Data:"))
        self.y_combo = QComboBox()
        self.y_combo.addItems(["Heart Rate", "Blood Pressure", "Temperature", "Oxygen Level"])
        self.y_combo.currentTextChanged.connect(self.update_visualization)
        data_layout.addWidget(self.y_combo)
        
        controls_layout.addWidget(data_group)
        
        # Plot Settings
        settings_group = QGroupBox("Plot Settings")
        settings_layout = QVBoxLayout(settings_group)
        
        # Window size slider
        window_label = QLabel("Window Size: 100%")
        self.window_slider = QSlider(Qt.Orientation.Horizontal)
        self.window_slider.setRange(10, 100)
        self.window_slider.setValue(100)
        self.window_slider.valueChanged.connect(
            lambda v: (window_label.setText(f"Window Size: {v}%"), self.update_visualization()))
        
        # Smoothing slider
        smoothing_label = QLabel("Smoothing: 0%")
        self.smoothing_slider = QSlider(Qt.Orientation.Horizontal)
        self.smoothing_slider.setRange(0, 100)
        self.smoothing_slider.setValue(0)
        self.smoothing_slider.valueChanged.connect(
            lambda v: (smoothing_label.setText(f"Smoothing: {v}%"), self.update_visualization()))
        
        for slider in [self.window_slider, self.smoothing_slider]:
            slider.setStyleSheet("""
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
            """)
        
        settings_layout.addWidget(window_label)
        settings_layout.addWidget(self.window_slider)
        settings_layout.addWidget(smoothing_label)
        settings_layout.addWidget(self.smoothing_slider)
        
        controls_layout.addWidget(settings_group)
        
        # Export controls
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout(export_group)
        
        export_button = QPushButton("Export Plot")
        export_button.clicked.connect(self.export_plot)
        export_layout.addWidget(export_button)
        
        controls_layout.addWidget(export_group)
        controls_layout.addStretch()
        
        # Right Panel - Visualization
        viz_panel = QWidget()
        viz_layout = QVBoxLayout(viz_panel)
        
        # Create matplotlib figure
        self.figure = plt.figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        viz_layout.addWidget(self.toolbar)
        viz_layout.addWidget(self.canvas)
        
        # Add panels to main layout
        main_layout.addWidget(controls_panel, stretch=1)
        main_layout.addWidget(viz_panel, stretch=3)
        
        # Initial plot
        self.update_visualization()
        
    def update_visualization(self):
        self.figure.clear()
        
        # Generate sample data (replace with real data in production)
        np.random.seed(0)
        t = np.linspace(0, 10, 1000)
        y = np.sin(t) + np.random.normal(0, 0.1, len(t))
        
        chart_type = self.chart_combo.currentText()
        
        if chart_type == "Time Series Plot":
            ax = self.figure.add_subplot(111)
            window = int(len(t) * self.window_slider.value() / 100)
            smoothing = self.smoothing_slider.value() / 100
            
            if smoothing > 0:
                kernel_size = int(max(3, smoothing * 100))
                kernel = np.ones(kernel_size) / kernel_size
                y = np.convolve(y, kernel, mode='same')
            
            ax.plot(t[:window], y[:window])
            ax.set_xlabel(self.x_combo.currentText())
            ax.set_ylabel(self.y_combo.currentText())
            ax.grid(True)
            
        elif chart_type == "Scatter Plot":
            ax = self.figure.add_subplot(111)
            ax.scatter(np.random.randn(100), np.random.randn(100), alpha=0.5)
            ax.set_xlabel(self.x_combo.currentText())
            ax.set_ylabel(self.y_combo.currentText())
            ax.grid(True)
            
        elif chart_type == "Heatmap":
            ax = self.figure.add_subplot(111)
            data = np.random.randn(10, 10)
            sns.heatmap(data, ax=ax, cmap='viridis')
            ax.set_xlabel("Variables")
            ax.set_ylabel("Variables")
            
        elif chart_type == "FFT Plot":
            ax = self.figure.add_subplot(111)
            fft = np.fft.fft(y)
            freq = np.fft.fftfreq(len(t), t[1] - t[0])
            ax.plot(freq[:len(freq)//2], np.abs(fft)[:len(freq)//2])
            ax.set_xlabel("Frequency")
            ax.set_ylabel("Magnitude")
            ax.grid(True)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def export_plot(self):
        self.figure.savefig('plot_export.png', dpi=300, bbox_inches='tight')