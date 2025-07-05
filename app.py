from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton)
import sys
from main import get_classes, convert_to_days, show_data

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Schedule GUI")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.launch_schedule_button = QPushButton("luanch from termianl logic")
        self.launch_schedule_button.clicked.connect(self.run_schedule_from_imported_logic)

        layout.addWidget(self.launch_schedule_button)
        self.setLayout(layout)

    def run_schedule_from_imported_logic(self):
        all_courses = get_classes()
        class_days = convert_to_days(all_courses)
        show_data(class_days)


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()






