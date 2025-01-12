# tab_widget.py
from PyQt6.QtWidgets import QTabWidget
from data_loading_tab import DataLoadingTab
from health_analysis_tab import HealthAnalysisTab
from spectrum_analysis_tab import SpectrumAnalysisTab
from image_processing_tab import ImageProcessingTab
from visualization_tab import VisualizationTab
from welcome_ui import WelcomeTab

class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_tabs()
    
    def setup_tabs(self):
        self.addTab(WelcomeTab(), "Welcome")
        self.addTab(DataLoadingTab(), "Data Loading")
        self.addTab(ImageProcessingTab(), "Image Processing")
        self.addTab(HealthAnalysisTab(), "Health Analysis")
        self.addTab(SpectrumAnalysisTab(), "Spectrum Analysis")
        self.addTab(VisualizationTab(), "Visualization")