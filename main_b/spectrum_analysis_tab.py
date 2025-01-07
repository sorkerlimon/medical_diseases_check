# spectrum_analysis_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QPushButton,
                            QComboBox, QSlider, QLabel)
from PyQt6.QtCore import Qt

class SpectrumAnalysisTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Signal loading section
        signal_group = QGroupBox("Signal Loading")
        signal_layout = QVBoxLayout(signal_group)
        
        signal_layout.addWidget(QPushButton("Load Signal"))
        combo = QComboBox()
        combo.addItems(["ECG", "EEG", "EMG"])
        signal_layout.addWidget(combo)
        
        # FFT Analysis section
        fft_group = QGroupBox("FFT Analysis")
        fft_layout = QVBoxLayout(fft_group)
        
        fft_layout.addWidget(QPushButton("Compute FFT"))
        fft_layout.addWidget(QLabel("Time Window:"))
        fft_layout.addWidget(QSlider(Qt.Orientation.Horizontal))
        
        layout.addWidget(signal_group)
        layout.addWidget(fft_group)
