import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QFileDialog, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QFileDialog, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SpectrumAnalysisApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize the GUI window
        self.setWindowTitle("Spectrum Analysis")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout for the GUI
        layout = QVBoxLayout()

        # Load Button
        self.load_button = QPushButton("Load Signal")
        self.load_button.clicked.connect(self.load_signal)
        layout.addWidget(self.load_button)

        # FFT Button
        self.fft_button = QPushButton("Compute FFT")
        self.fft_button.clicked.connect(self.compute_fft)
        layout.addWidget(self.fft_button)

        # Slider for time window selection
        self.time_window_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_window_slider.setRange(0, 100)
        self.time_window_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.time_window_slider.setTickInterval(1)
        self.time_window_slider.valueChanged.connect(self.update_fft)  # Dynamic update on slider change
        layout.addWidget(QLabel("Select Time Window"))
        layout.addWidget(self.time_window_slider)

        # Matplotlib figure and axis
        self.fig, self.ax = plt.subplots()
        self.canvas = None
        self.setLayout(layout)

    def load_signal(self):
        """Load the biomedical signal (e.g., ECG/EEG) from a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            # Use np.genfromtxt to skip the header
            data = np.genfromtxt(file_path, delimiter=',', skip_header=1)  # Skipping the header row
            self.time = data[:, 0]  # Assuming the first column is the time
            self.signal = data[:, 1]  # Assuming the second column is the amplitude
            self.plot_signal()

    def plot_signal(self):
        """Display the raw signal."""
        self.ax.clear()
        self.ax.plot(self.time, self.signal)
        self.ax.set_title("Raw Signal")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        
        # Update the canvas
        if self.canvas:
            self.canvas.draw()
        else:
            self.canvas = FigureCanvas(self.fig)
            layout = self.layout()
            layout.addWidget(self.canvas)
            self.canvas.draw()

    def compute_fft(self):
        """Compute and plot the FFT of the signal."""
        start_idx = self.time_window_slider.value()
        window_size = 100  # Define a fixed window size for FFT
        
        # Slice the signal based on the selected time window
        end_idx = start_idx + window_size
        signal_segment = self.signal[start_idx:end_idx]
        
        # Perform FFT
        n = len(signal_segment)
        freq = np.fft.fftfreq(n, d=(self.time[1] - self.time[0]))  # Frequency axis
        spectrum = fft(signal_segment)
        power_spectrum = np.abs(spectrum)**2  # Power spectrum
        
        # Plot the frequency spectrum
        self.ax.clear()
        self.ax.plot(freq[:n//2], power_spectrum[:n//2])  # Plot only the positive frequencies
        self.ax.set_title("Power Spectrum")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Power")
        
        # Update the canvas
        if self.canvas:
            self.canvas.draw()

    def update_fft(self):
        """Update FFT plot dynamically when slider value changes."""
        self.compute_fft()  # Recompute FFT with new time window slider value

if __name__ == "__main__":
    app = QApplication([])
    window = SpectrumAnalysisApp()
    window.show()
    app.exec()

class SpectrumAnalysisApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize the GUI window
        self.setWindowTitle("Spectrum Analysis")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout for the GUI
        layout = QVBoxLayout()

        # Load Button
        self.load_button = QPushButton("Load Signal")
        self.load_button.clicked.connect(self.load_signal)
        layout.addWidget(self.load_button)

        # FFT Button
        self.fft_button = QPushButton("Compute FFT")
        self.fft_button.clicked.connect(self.compute_fft)
        layout.addWidget(self.fft_button)

        # Slider for time window selection
        self.time_window_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_window_slider.setRange(0, 100)
        self.time_window_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.time_window_slider.setTickInterval(1)
        self.time_window_slider.valueChanged.connect(self.update_fft)  # Dynamic update on slider change
        layout.addWidget(QLabel("Select Time Window"))
        layout.addWidget(self.time_window_slider)

        # Matplotlib figure and axis
        self.fig, self.ax = plt.subplots()
        self.canvas = None
        self.setLayout(layout)

    def load_signal(self):
        """Load the biomedical signal (e.g., ECG/EEG) from a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            # Use np.genfromtxt to skip the header
            data = np.genfromtxt(file_path, delimiter=',', skip_header=1)  # Skipping the header row
            self.time = data[:, 0]  # Assuming the first column is the time
            self.signal = data[:, 1]  # Assuming the second column is the amplitude
            self.plot_signal()

    def plot_signal(self):
        """Display the raw signal."""
        self.ax.clear()
        self.ax.plot(self.time, self.signal)
        self.ax.set_title("Raw Signal")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        
        # Update the canvas
        if self.canvas:
            self.canvas.draw()
        else:
            self.canvas = FigureCanvas(self.fig)
            layout = self.layout()
            layout.addWidget(self.canvas)
            self.canvas.draw()

    def compute_fft(self):
        """Compute and plot the FFT of the signal."""
        start_idx = self.time_window_slider.value()
        window_size = 100  # Define a fixed window size for FFT
        
        # Slice the signal based on the selected time window
        end_idx = start_idx + window_size
        signal_segment = self.signal[start_idx:end_idx]
        
        # Perform FFT
        n = len(signal_segment)
        freq = np.fft.fftfreq(n, d=(self.time[1] - self.time[0]))  # Frequency axis
        spectrum = fft(signal_segment)
        power_spectrum = np.abs(spectrum)**2  # Power spectrum
        
        # Plot the frequency spectrum
        self.ax.clear()
        self.ax.plot(freq[:n//2], power_spectrum[:n//2])  # Plot only the positive frequencies
        self.ax.set_title("Power Spectrum")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Power")
        
        # Update the canvas
        if self.canvas:
            self.canvas.draw()

    def update_fft(self):
        """Update FFT plot dynamically when slider value changes."""
        self.compute_fft()  # Recompute FFT with new time window slider value

if __name__ == "__main__":
    app = QApplication([])
    window = SpectrumAnalysisApp()
    window.show()
    app.exec()
