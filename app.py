from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit)
import sys
from main import get_classes, convert_to_days, show_data

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Schedule GUI")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        #classes enter
        self.label1 = QLabel('Class: ')
        layout.addWidget(self.label1)
        self.input_box1 = QLineEdit()
        layout.addWidget(self.input_box1)

        #days enter
        self.label2 = QLabel('Days (m, t, w, th, f): ')
        layout.addWidget(self.label2)
        self.input_box2 = QLineEdit()
        layout.addWidget(self.input_box2)

        #times enter
        self.label3 = QLabel('time (start-finish): ')
        layout.addWidget(self.label3)
        self.input_box3 = QLineEdit()
        layout.addWidget(self.input_box3)



        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.process_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def process_input(self):
        class_name = self.input_box1.text()
        days = self.input_box2.text()
        time_range = self.input_box3.text()

        print(f"Class: {class_name}")
        print(f"Days: {days}")
        print(f"Time: {time_range}")


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()






