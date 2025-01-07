# spectrum_analysis_tab.py
import numpy as np
from scipy.fft import fft
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QComboBox, QSlider, QFileDialog)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class SpectrumAnalysisTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time = None
        self.signal = None
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Left panel (Original Signal)
        left_panel = QGroupBox("Original Signal")
        left_layout = QVBoxLayout(left_panel)
        
        # Load button
        self.load_button = QPushButton("Load Signal")
        self.load_button.clicked.connect(self.load_signal)
        left_layout.addWidget(self.load_button)
        
        # Original signal plot
        self.original_fig = plt.figure(figsize=(6, 4))
        self.original_canvas = FigureCanvas(self.original_fig)
        self.original_toolbar = NavigationToolbar(self.original_canvas, self)
        left_layout.addWidget(self.original_toolbar)
        left_layout.addWidget(self.original_canvas)
        
        # Center panel (Controls)
        center_panel = QGroupBox("Analysis Controls")
        center_layout = QVBoxLayout(center_panel)
        
        # Analysis method selection
        center_layout.addWidget(QLabel("Analysis Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Power Spectrum",
            "Magnitude Spectrum",
            "Phase Spectrum"
        ])
        self.method_combo.currentTextChanged.connect(self.update_spectrum)
        center_layout.addWidget(self.method_combo)
        
        # Window settings
        window_group = QGroupBox("Window Settings")
        window_layout = QVBoxLayout(window_group)
        
        # Window size slider
        window_size_label = QLabel("Window Size: 100%")
        self.window_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.window_size_slider.setRange(10, 100)
        self.window_size_slider.setValue(100)
        self.window_size_slider.valueChanged.connect(
            lambda v: (window_size_label.setText(f"Window Size: {v}%"), self.update_spectrum()))
        
        # Window position slider
        window_pos_label = QLabel("Window Position: 0%")
        self.window_pos_slider = QSlider(Qt.Orientation.Horizontal)
        self.window_pos_slider.setRange(0, 100)
        self.window_pos_slider.setValue(0)
        self.window_pos_slider.valueChanged.connect(
            lambda v: (window_pos_label.setText(f"Window Position: {v}%"), self.update_spectrum()))
        
        # Add sliders to window group
        window_layout.addWidget(window_size_label)
        window_layout.addWidget(self.window_size_slider)
        window_layout.addWidget(window_pos_label)
        window_layout.addWidget(self.window_pos_slider)
        center_layout.addWidget(window_group)
        
        # Frequency settings
        freq_group = QGroupBox("Frequency Settings")
        freq_layout = QVBoxLayout(freq_group)
        
        freq_range_label = QLabel("Frequency Range: 100%")
        self.freq_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.freq_range_slider.setRange(10, 100)
        self.freq_range_slider.setValue(100)
        self.freq_range_slider.valueChanged.connect(
            lambda v: (freq_range_label.setText(f"Frequency Range: {v}%"), self.update_spectrum()))
        
        freq_layout.addWidget(freq_range_label)
        freq_layout.addWidget(self.freq_range_slider)
        center_layout.addWidget(freq_group)
        
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
        
        for slider in [self.window_size_slider, self.window_pos_slider, self.freq_range_slider]:
            slider.setStyleSheet(slider_style)
        
        center_layout.addStretch()
        
        # Right panel (Spectrum)
        right_panel = QGroupBox("Spectrum Analysis")
        right_layout = QVBoxLayout(right_panel)
        
        # Spectrum plot
        self.spectrum_fig = plt.figure(figsize=(6, 4))
        self.spectrum_canvas = FigureCanvas(self.spectrum_fig)
        self.spectrum_toolbar = NavigationToolbar(self.spectrum_canvas, self)
        right_layout.addWidget(self.spectrum_toolbar)
        right_layout.addWidget(self.spectrum_canvas)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(center_panel)
        main_layout.addWidget(right_panel)
    
    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", 
                                                 "CSV Files (*.csv);;All Files (*)")
        if file_path:
            try:
                data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
                self.time = data[:, 0]
                self.signal = data[:, 1]
                self.plot_signal()
                self.update_spectrum()
            except Exception as e:
                print(f"Error loading file: {e}")
    
    def plot_signal(self):
        if self.signal is None:
            return
            
        self.original_fig.clear()
        ax = self.original_fig.add_subplot(111)
        ax.plot(self.time, self.signal)
        ax.set_title("Original Signal")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        self.original_fig.tight_layout()
        self.original_canvas.draw()
    
    def update_spectrum(self):
        if self.signal is None:
            return
            
        # Get window parameters
        window_size = int(len(self.signal) * self.window_size_slider.value() / 100)
        start_pos = int(len(self.signal) * self.window_pos_slider.value() / 100)
        
        # Extract signal segment
        end_pos = min(start_pos + window_size, len(self.signal))
        signal_segment = self.signal[start_pos:end_pos]
        time_segment = self.time[start_pos:end_pos]
        
        # Compute FFT
        n = len(signal_segment)
        freq = np.fft.fftfreq(n, d=(time_segment[1] - time_segment[0]))
        spectrum = fft(signal_segment)
        
        # Plot based on selected method
        self.spectrum_fig.clear()
        ax = self.spectrum_fig.add_subplot(111)
        
        method = self.method_combo.currentText()
        freq_range = int(len(freq)//2 * self.freq_range_slider.value() / 100)
        
        if method == "Power Spectrum":
            power_spectrum = np.abs(spectrum)**2
            ax.plot(freq[:freq_range], power_spectrum[:freq_range])
            ax.set_ylabel("Power")
        elif method == "Magnitude Spectrum":
            magnitude_spectrum = np.abs(spectrum)
            ax.plot(freq[:freq_range], magnitude_spectrum[:freq_range])
            ax.set_ylabel("Magnitude")
        elif method == "Phase Spectrum":
            phase_spectrum = np.angle(spectrum)
            ax.plot(freq[:freq_range], phase_spectrum[:freq_range])
            ax.set_ylabel("Phase (radians)")
        
        ax.set_title(f"{method}")
        ax.set_xlabel("Frequency (Hz)")
        ax.grid(True)
        
        self.spectrum_fig.tight_layout()
        self.spectrum_canvas.draw()