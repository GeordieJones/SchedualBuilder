from PySide6.QtWidgets import QApplication
from orgainzed_app.ui.windows import MainWindow
import sys

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run_app()