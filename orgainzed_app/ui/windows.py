import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                                QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal

from orgainzed_app.core.data import ScheduleManager
from orgainzed_app.core.scheduler import optimize_schedule

class ClassInputWindow(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Input")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()
        # Class name
        layout.addWidget(QLabel('Class:'), 0, 0)
        self.input_name = QLineEdit()
        self.input_name.setMinimumWidth(300)
        layout.addWidget(self.input_name, 0, 1)
        # Days
        layout.addWidget(QLabel('Days (m t w th f):'), 1, 0)
        self.input_days = QLineEdit()
        layout.addWidget(self.input_days, 1, 1)
        # Time
        layout.addWidget(QLabel('Time (start-end AM/PM):'), 2, 0)
        self.input_time = QLineEdit()
        layout.addWidget(self.input_time, 2, 1)
        # Difficulty
        layout.addWidget(QLabel('Difficulty:'), 3, 0)
        self.input_diff = QLineEdit()
        layout.addWidget(self.input_diff, 3, 1)
        # Buttons
        self.submit_btn = QPushButton('Submit Class')
        self.submit_btn.clicked.connect(self.process_input)
        layout.addWidget(self.submit_btn, 4, 0)
        self.next_btn = QPushButton('Next')
        self.next_btn.clicked.connect(self.on_next)
        layout.addWidget(self.next_btn, 4, 1)
        self.setLayout(layout)

    def process_input(self):
        try:
            name = self.input_name.text()
            days = self.input_days.text().split()
            time_str, mer = self.input_time.text().split()
            start, end = time_str.split('-')
            diff = int(self.input_diff.text())
            data = {'name': name, 'days': days, 'start': start,
                    'end': end, 'meridian': mer, 'difficulty': diff}
            self.submitted.emit(data)
            # clear
            for w in [self.input_name, self.input_days, self.input_time, self.input_diff]:
                w.clear()
        except Exception as e:
            print(f"Error processing class input: {e}")

    def on_next(self):
        self.close()
        self.parent().show_activity_window()

class ActivityInputWindow(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Activity Input")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()
        layout.addWidget(QLabel('Activity:'), 0, 0)
        self.input_name = QLineEdit(); self.input_name.setMinimumWidth(300)
        layout.addWidget(self.input_name, 0, 1)
        layout.addWidget(QLabel('Days (m t w th f):'), 1, 0)
        self.input_days = QLineEdit()
        layout.addWidget(self.input_days, 1, 1)
        layout.addWidget(QLabel('Time (start-end AM/PM):'), 2, 0)
        self.input_time = QLineEdit()
        layout.addWidget(self.input_time, 2, 1)
        self.submit_btn = QPushButton('Submit Activity')
        self.submit_btn.clicked.connect(self.process_input)
        layout.addWidget(self.submit_btn, 3, 0)
        self.next_btn = QPushButton('Next')
        self.next_btn.clicked.connect(self.on_next)
        layout.addWidget(self.next_btn, 3, 1)
        self.setLayout(layout)

    def process_input(self):
        try:
            name = self.input_name.text()
            days = self.input_days.text().split()
            time_str, mer = self.input_time.text().split()
            start, end = time_str.split('-')
            data = {'name': name, 'days': days,
                    'start': start, 'end': end, 'meridian': mer}
            self.submitted.emit(data)
            for w in [self.input_name, self.input_days, self.input_time]:
                w.clear()
        except Exception as e:
            print(f"Error processing activity input: {e}")

    def on_next(self):
        self.close()
        self.parent().show_prefs_window()

class PreferencesWindow(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preferences")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()
        layout.addWidget(QLabel('Start willing to start:'), 0, 0)
        self.input_start = QLineEdit(); self.input_start.setMinimumWidth(300)
        layout.addWidget(self.input_start, 0, 1)
        layout.addWidget(QLabel('End willing to end:'), 1, 0)
        self.input_end = QLineEdit()
        layout.addWidget(self.input_end, 1, 1)
        layout.addWidget(QLabel('Max hours:'), 2, 0)
        self.input_max = QLineEdit()
        layout.addWidget(self.input_max, 2, 1)
        layout.addWidget(QLabel('Min hours:'), 3, 0)
        self.input_min = QLineEdit()
        layout.addWidget(self.input_min, 3, 1)
        self.submit_btn = QPushButton('Submit Preferences')
        self.submit_btn.clicked.connect(self.process_input)
        layout.addWidget(self.submit_btn, 4, 0)
        self.finish_btn = QPushButton('Finish')
        self.finish_btn.clicked.connect(self.on_finish)
        layout.addWidget(self.finish_btn, 4, 1)
        self.setLayout(layout)

    def process_input(self):
        try:
            data = {
                'start_time': self.input_start.text(),
                'end_time': self.input_end.text(),
                'max_hours': int(self.input_max.text()),
                'min_hours': int(self.input_min.text())
            }
            self.submitted.emit(data)
        except Exception as e:
            print(f"Error processing preferences: {e}")

    def on_finish(self):
        self.close()
        self.parent().show_schedule()

class ScheduleDisplayWindow(QWidget):
    def __init__(self, schedule_data):
        super().__init__()
        self.schedule_data = schedule_data
        self.setWindowTitle("Schedule Display")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        table = QTableWidget()
        table.setRowCount(len(self.schedule_data))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Day','Schedule','Classes','Activities','Study'])
        name_map = {'m':'Monday','t':'Tuesday','w':'Wednesday','th':'Thursday','f':'Friday','sat':'Saturday','sun':'Sunday'}
        # prepare combined function on manager
        for i, day in enumerate(self.schedule_data):
            day_name = name_map.get(day.name, day.name)
            # classes
            cls = '\n'.join(f"{c.name} ({c.time_range()})" for c in day.courses) or 'No classes'
            acts = '\n'.join(f"{a.name} ({a.time_range()})" for a in day.activities) or 'No activities'
            studs = '\n'.join(f"{s.name} ({s.time_range()})" for s in day.study_times) or 'No study sessions'
            all_items = self.schedule_data.get_sorted_daily_items(day.name) or ['No items']
            # set items
            table.setItem(i,0,QTableWidgetItem(day_name))
            table.setItem(i,1,QTableWidgetItem('\n'.join(all_items)))
            table.setItem(i,2,QTableWidgetItem(cls))
            table.setItem(i,3,QTableWidgetItem(acts))
            table.setItem(i,4,QTableWidgetItem(studs))
        table.resizeColumnsToContents(); table.resizeRowsToContents(); table.setWordWrap(True)
        layout = QVBoxLayout(); layout.addWidget(table); self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = ScheduleManager()
        self.setup_navigation()

    def setup_navigation(self):
        # Initialize input windows without setting them as direct children
        self.class_win = ClassInputWindow()
        self.act_win = ActivityInputWindow()
        self.pref_win = PreferencesWindow()

        # Connect navigation callbacks from buttons rather than relying on parent-child
        self.class_win.submitted.connect(self.manager.add_course)
        self.class_win.next_btn.clicked.connect(self.show_activity_window)

        self.act_win.submitted.connect(self.manager.add_activity)
        self.act_win.next_btn.clicked.connect(self.show_prefs_window)

        self.pref_win.submitted.connect(self.manager.set_preferences)
        self.pref_win.finish_btn.clicked.connect(self.show_schedule)

        # Show the first window
        self.show_class_window()

    def show_class_window(self):
        # Ensure only the class window is visible
        for w in (self.act_win, self.pref_win): w.hide()
        self.class_win.show()

    def show_activity_window(self):
        # Hide others and show activity input
        self.class_win.hide()
        self.pref_win.hide()
        self.act_win.show()

    def show_prefs_window(self):
        # Hide others and show preferences input
        self.class_win.hide()
        self.act_win.hide()
        self.pref_win.show()

    def show_schedule(self):
        # Hide input windows and display final schedule
        self.class_win.hide()
        self.act_win.hide()
        self.pref_win.hide()
        sched = optimize_schedule(self.manager)
        self.display = ScheduleDisplayWindow(sched)
        self.display.show()


    def show_class_window(self): self.class_win.show()
    def show_activity_window(self): self.act_win.show()
    def show_prefs_window(self): self.pref_win.show()

    def show_schedule(self):
        sched = optimize_schedule(self.manager)
        self.display = ScheduleDisplayWindow(sched)
        self.display.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec())
