# visualization_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QComboBox

class VisualizationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Chart selection
        viz_group = QGroupBox("Visualization Options")
        viz_layout = QVBoxLayout(viz_group)
        
        chart_combo = QComboBox()
        chart_combo.addItems([
            "Time Series Plot",
            "Scatter Plot",
            "Heatmap",
            "FFT Plot"
        ])
        
        viz_layout.addWidget(chart_combo)
        
        # Plot area
        plot_area = QWidget()
        
        layout.addWidget(viz_group)
        layout.addWidget(plot_area)