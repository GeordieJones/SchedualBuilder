from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit)
import sys
from main import get_classes, convert_to_days, show_data

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Schedule GUI")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Eneter class: ')
        layout.addWidget(self.label)
        self.input_box = QLineEdit()
        layout.addWidget(self.input_box)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.process_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def process_input(self):
        user_input = self.input_box.text()
        print(f'Input: {user_input}')


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()






