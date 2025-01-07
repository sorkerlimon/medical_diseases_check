# main.py
from PyQt6.QtWidgets import QApplication
from main_window import HealthcareMainWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = HealthcareMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()