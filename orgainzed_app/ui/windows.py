from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                                QLineEdit, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                                QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal

from orgainzed_app.core.data import ScheduleManager
from orgainzed_app.core.scheduler import optimize_schedule

class firstWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
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
            course_data = {
                'name': self.input_box1.text(),
                'days': self.input_box2.text().split(),  # e.g., ['m', 'w', 'f']
                'start': self.input_box3.text().split()[0].split('-')[0],  # e.g., '9'
                'end': self.input_box3.text().split()[0].split('-')[1],    # e.g., '10'
                'meridian': self.input_box3.text().split()[1],             # e.g., 'am'
                'difficulty': int(self.input_box4.text())
            }

            self.manager.add_course(course_data)

            print(f"Class: {course_data['name']}")
            print(f"Days: {course_data['days']}")
            print(f"Time: {course_data['start']}-{course_data['end']} {course_data['meridian']}")
            print(f"Diff: {course_data['difficulty']}")

            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()
            self.input_box4.clear()

        except Exception as e:
                print(f"Error: {e}")

    def next_page(self):
        self.close()
        self.activity_window = secondWindow(self.manager)
        self.activity_window.show()

class secondWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
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
            activity_data = {
                'name': self.input_box1.text(),
                'days': self.input_box2.text().split(),  # e.g., ['m', 'w', 'f']
                'start': self.input_box3.text().split()[0].split('-')[0],  # e.g., '9'
                'end': self.input_box3.text().split()[0].split('-')[1],    # e.g., '10'
                'meridian': self.input_box3.text().split()[1],             # e.g., 'am'
            }

            self.manager.add_activity(activity_data)
            print(f"Activity: {activity_data['name']}")
            print(f"Days: {activity_data['days']}")
            print(f"Time: {activity_data['start']}-{activity_data['end']} {activity_data['meridian']}")

            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()

        except Exception as e:
                print(f"Error: {e}")

    def next_page(self):
        self.close()
        self.activity_window = thirdWindow(self.manager)
        self.activity_window.show()

class thirdWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
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
            value_data = {
                'start': self.input_box1.text(),
                'end': self.input_box2.text(),  # e.g., ['m', 'w', 'f']
                'max': float(self.input_box3.text()),  # e.g., '9 AM'
                'min': float(self.input_box4.text())    # e.g., '10 PM'
            }

            self.finish(value_data)

        except Exception as e:
                print(f"Error: {e}")

    def finish(self,value_data):
        self.input_box1.setDisabled(True)
        self.input_box2.setDisabled(True)
        self.input_box3.setDisabled(True)
        self.submit_button.setDisabled(True)
        self.finish_button.setDisabled(True)

        self.close()

        self.schedule_window = showData(self.manager, value_data)
        self.schedule_window.show()


class showData(QTableWidget):
    def __init__(self, manager, value_data):
        super().__init__()
        self.manager = optimize_schedule(manager, value_data)  # Update manager with study sessions

        self.setWindowTitle("Optimized Schedule")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)

        day_name_map = {
            'm': 'Monday',
            't': 'Tuesday',
            'w': 'Wednesday',
            'th': 'Thursday',
            'f': 'Friday',
            'sat': 'Saturday',
            'sun': 'Sunday'
        }

        day_schedules = self.manager.day_schedules

        self.setRowCount(len(day_schedules))
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Day', 'Schedule'])

        for row, (day_key, schedule_obj) in enumerate(day_schedules.items()):
            # Day name
            self.setItem(row, 0, QTableWidgetItem(day_name_map.get(day_key, day_key.capitalize())))

            # Combined daily items (classes, activities, study sessions)
            schedule_text = "\n".join(self.manager.get_sorted_daily_items(day_key))
            self.setItem(row, 1, QTableWidgetItem(schedule_text))

        self.resizeColumnsToContents()
        self.resizeRowsToContents()


def run():
    app = QApplication(sys.argv)
    manager = ScheduleManager()
    window = firstWindow(manager)
    window.show()
    sys.exit(app.exec())
