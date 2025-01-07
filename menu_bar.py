# menu_bar.py
from PyQt6.QtWidgets import QMenuBar, QMessageBox, QDialog, QVBoxLayout, QLabel, QTextBrowser
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

class HelpDialog(QDialog):
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Create text browser for documentation
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml(content)
        
        layout.addWidget(text_browser)
        
        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QTextBrowser {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }
        """)

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenuBar {
                background-color: #2c3e50;
                color: white;
                min-height: 28px;
                padding: 2px;
            }
            QMenuBar::item {
                spacing: 5px;
                padding: 4px 12px;
                background: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background: #34495e;
            }
            QMenu {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                padding: 5px;
            }
            QMenu::item {
                padding: 6px 32px 6px 20px;
                border-radius: 3px;
                min-width: 120px;
            }
            QMenu::item:selected {
                background: #3498db;
            }
        """)
        self.create_menus()
        
    def create_menus(self):
        # File menu (keeping existing code)
        file_menu = self.addMenu("File")
        file_menu.addAction(QAction("Load Data", self))
        file_menu.addAction(QAction("Save", self))
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        # exit_action.triggered.connect(self.parent().close)
        exit_action.triggered.connect(self.confirm_exit)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = self.addMenu("View")
        
        # Help menu
        help_menu = self.addMenu("Help")
        
        # Documentation action
        doc_action = QAction("Documentation", self)
        doc_action.setStatusTip("View detailed documentation")
        doc_action.triggered.connect(self.show_documentation)
        help_menu.addAction(doc_action)
        
        # Quick Start Guide action
        quickstart_action = QAction("Quick Start Guide", self)
        quickstart_action.setStatusTip("View quick start tutorial")
        quickstart_action.triggered.connect(self.show_quickstart)
        help_menu.addAction(quickstart_action)
        
        help_menu.addSeparator()
        
        # About action
        about_action = QAction("About", self)
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def confirm_exit(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Exit")
        msg_box.setText("Are you sure you want to exit?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        # Styling the message box
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f5f5f5;
            }
            QPushButton {
                min-width: 80px;
                padding: 5px;
                border: none;
                border-radius: 4px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f638a;
            }
        """)

        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.parent().close()

    def show_documentation(self):
        content = """
        <h2>Healthcare Data Analysis Tool Documentation</h2>
        <h3>Features</h3>
        <ul>
            <li><b>Data Loading</b>: Import and manage healthcare data
                <ul>
                    <li>Support for CSV files</li>
                    <li>Data preview capabilities</li>
                </ul>
            </li>
            <li><b>Health Analysis</b>: Analyze health metrics
                <ul>
                    <li>Statistical analysis</li>
                    <li>Trend identification</li>
                </ul>
            </li>
            <li><b>Spectrum Analysis</b>: Process and analyze signal data
                <ul>
                    <li>FFT analysis</li>
                    <li>Signal filtering</li>
                </ul>
            </li>
            <li><b>Image Processing</b>: Medical image analysis tools
                <ul>
                    <li>Image enhancement</li>
                    <li>Feature detection</li>
                </ul>
            </li>
            <li><b>Visualization</b>: Data visualization tools
                <ul>
                    <li>Interactive charts</li>
                    <li>Custom plotting options</li>
                </ul>
            </li>
        </ul>
        """
        dialog = HelpDialog("Documentation", content, self)
        dialog.exec()
    
    def show_quickstart(self):
        content = """
        <h2>Quick Start Guide</h2>
        <p>Follow these steps to get started:</p>
        <ol>
            <li><b>Load Your Data</b>
                <br>Use File > Load Data to import your healthcare data files
            </li>
            <li><b>Choose Analysis Type</b>
                <br>Select the appropriate tab for your analysis needs
            </li>
            <li><b>Process Data</b>
                <br>Use the available tools to process and analyze your data
            </li>
            <li><b>Visualize Results</b>
                <br>Create visualizations of your analysis results
            </li>
            <li><b>Save Your Work</b>
                <br>Use File > Save to preserve your results
            </li>
        </ol>
        <p>For more detailed information, please refer to the full documentation.</p>
        """
        dialog = HelpDialog("Quick Start Guide", content, self)
        dialog.exec()
    
    def show_about(self):
        QMessageBox.about(
            self,
            "About Healthcare Data Analysis Tool",
            """<h3>Healthcare Data Analysis Tool</h3>
            <p>Version 1.0</p>
            <p>A comprehensive tool for healthcare data analysis and visualization.</p>
            <p>Features:</p>
            <ul>
                <li>Data analysis</li>
                <li>Health metrics tracking</li>
                <li>Signal processing</li>
                <li>Medical image analysis</li>
                <li>Interactive visualizations</li>
            </ul>"""
        )