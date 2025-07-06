from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit)
import sys
import main


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
        self.label3 = QLabel('time (start-finish AM/PM): ')
        layout.addWidget(self.label3)
        self.input_box3 = QLineEdit()
        layout.addWidget(self.input_box3)



        self.submit_button = QPushButton("Submit class")
        self.submit_button.clicked.connect(self.process_input)
        layout.addWidget(self.submit_button)

        self.finish_button = QPushButton("Finish")
        self.finish_button.clicked.connect(self.finish)
        layout.addWidget(self.finish_button)

        self.setLayout(layout)

    def process_input(self):
        try:
            class_name = self.input_box1.text()
            days = self.input_box2.text().split()
            time_range = self.input_box3.text()

            time_string, period = time_range.split()
            start, end = time_string.split('-')

            main.add_class(class_name, days, start, end, period)

            print(f"Class: {class_name}")
            print(f"Days: {days}")
            print(f"Time: {start}-{end} {period}")

            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()

        except Exception as e:
                print(f"Error: {e}")

    def finish(self):
        self.input_box1.setDisabled(True)
        self.input_box2.setDisabled(True)
        self.input_box3.setDisabled(True)
        self.submit_button.setDisabled(True)
        self.finish_button.setDisabled(True)

        self.close()

        self.schedule_window = main.show_data(main.class_days)
        self.schedule_window.show()


def run_app():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run_app()






