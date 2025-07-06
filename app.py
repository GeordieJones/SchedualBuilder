from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                                QLineEdit, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt
import sys
import main

'''

last notes: currently added buttons and classes but now need to add a class difficulty and
            maybe assignments, tests, and projects in-order to give the details needed to build
            the optimizer program

'''

class firstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Schedule GUI")
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()

        #classes enter
        self.label1 = QLabel('Class: ')
        self.input_box1 = QLineEdit()
        self.input_box1.setMinimumWidth(300)
        layout.addWidget(self.label1, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box1, 0, 1)

        #days enter
        self.label2 = QLabel('Days (m, t, w, th, f): ')
        self.input_box2 = QLineEdit()
        layout.addWidget(self.label2, 1, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box2, 1, 1)

        #times enter
        self.label3 = QLabel('time (start-finish AM/PM): ')
        self.input_box3 = QLineEdit()
        layout.addWidget(self.label3, 2, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box3, 2, 1)

        self.label4 = QLabel('difficulty of class: ')
        self.input_box4 = QLineEdit()
        layout.addWidget(self.label4, 3, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box4, 3, 1)



        self.submit_button = QPushButton("Submit class")
        self.submit_button.setFixedSize(150, 40)
        layout.addWidget(self.submit_button, 4, 0)
        self.submit_button.clicked.connect(self.process_input)


        self.next_button = QPushButton("Next page")
        self.next_button.setFixedSize(150, 40)
        layout.addWidget(self.next_button, 4, 2)
        self.next_button.clicked.connect(self.next_page)


        self.setLayout(layout)

    def process_input(self):
        try:
            class_name = self.input_box1.text()
            days = self.input_box2.text().split()
            time_range = self.input_box3.text()
            diff = int(self.input_box4.text())

            time_string, period = time_range.split()
            start, end = time_string.split('-')

            main.add_class(class_name, days, start, end, period,diff)

            print(f"Class: {class_name}")
            print(f"Days: {days}")
            print(f"Time: {start}-{end} {period}")
            print(f"Diff: {diff}")

            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()
            self.input_box4.clear()

        except Exception as e:
                print(f"Error: {e}")

    def next_page(self):
        self.close()
        self.activity_window = secondWindow()
        self.activity_window.show()

class secondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Schedule GUI")
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()

        self.label1 = QLabel('Activity: ')
        self.input_box1 = QLineEdit()
        self.input_box1.setMinimumWidth(300)
        layout.addWidget(self.label1, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box1, 0, 1)

        self.label2 = QLabel('Days (m, t, w, th, f): ')
        self.input_box2 = QLineEdit()
        layout.addWidget(self.label2, 1, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box2, 1, 1)

        self.label3 = QLabel('time (start-finish AM/PM): ')
        self.input_box3 = QLineEdit()
        layout.addWidget(self.label3, 2, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box3, 2, 1)



        self.submit_button = QPushButton("Submit activity")
        self.submit_button.setFixedSize(150, 40)
        layout.addWidget(self.submit_button, 3, 0)
        self.submit_button.clicked.connect(self.process_input)


        self.finish_button = QPushButton("Next page")
        self.finish_button.setFixedSize(150, 40)
        layout.addWidget(self.finish_button, 3, 2)
        self.finish_button.clicked.connect(self.next_page)


        self.setLayout(layout)

    def process_input(self):
        try:
            activity_name = self.input_box1.text()
            days = self.input_box2.text().split()
            time_range = self.input_box3.text()

            time_string, period = time_range.split()
            start, end = time_string.split('-')

            main.add_activity(activity_name, days, start, end, period)

            print(f"Activity: {activity_name}")
            print(f"Days: {days}")
            print(f"Time: {start}-{end} {period}")

            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()

        except Exception as e:
                print(f"Error: {e}")

    def next_page(self):
        self.close()
        self.activity_window = thirdWindow()
        self.activity_window.show()



class thirdWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Schedule GUI")
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()

        #classes enter
        self.start = QLabel('Time willing to start: ')
        self.input_box1 = QLineEdit()
        self.input_box1.setMinimumWidth(300)
        layout.addWidget(self.start, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box1, 0, 1)

        #days enter
        self.end = QLabel('Time willing to end: ')
        self.input_box2 = QLineEdit()
        layout.addWidget(self.end, 1, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box2, 1, 1)

        #times enter
        self.max = QLabel('max hours: ')
        self.input_box3 = QLineEdit()
        layout.addWidget(self.max, 2, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box3, 2, 1)

        self.min = QLabel('min hours: ')
        self.input_box4 = QLineEdit()
        layout.addWidget(self.min, 3, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box4, 3, 1)



        self.submit_button = QPushButton("Submit hours")
        self.submit_button.setFixedSize(150, 40)
        layout.addWidget(self.submit_button, 4, 0)
        self.submit_button.clicked.connect(self.process_input)


        self.finish_button = QPushButton("Finish")
        self.finish_button.setFixedSize(150, 40)
        layout.addWidget(self.finish_button, 4, 2)
        self.finish_button.clicked.connect(self.finish)


        self.setLayout(layout)

    def process_input(self):
        try:
            start = self.input_box1.text()
            end = self.input_box2.text().split()
            max_val = int(self.input_box3.text())
            min_val = int(self.input_box4.text())

            main.add_values(start, end, max_val, min_val)

            print(f"time: {start} - {end}")
            print(f"max: {max_val}")
            print(f"min: {min_val}")

            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()
            self.input_box4.clear()

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
    window = firstWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run_app()






