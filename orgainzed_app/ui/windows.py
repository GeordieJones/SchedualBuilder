from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, 
                                QLabel, QLineEdit, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal
from core.data import ScheduleManager
from orgainzed_app.core.data import optimize_schedule

class ClassInputWindow(QWidget):
    submitted = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Schedule GUI")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QGridLayout()

        # Class input
        self.label1 = QLabel('Class: ')
        self.input_box1 = QLineEdit()
        self.input_box1.setMinimumWidth(300)
        layout.addWidget(self.label1, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box1, 0, 1)

        # Days input
        self.label2 = QLabel('Days (m, t, w, th, f): ')
        self.input_box2 = QLineEdit()
        layout.addWidget(self.label2, 1, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box2, 1, 1)

        # Time input
        self.label3 = QLabel('Time (start-finish AM/PM): ')
        self.input_box3 = QLineEdit()
        layout.addWidget(self.label3, 2, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box3, 2, 1)

        # Difficulty input
        self.label4 = QLabel('Difficulty of class: ')
        self.input_box4 = QLineEdit()
        layout.addWidget(self.label4, 3, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box4, 3, 1)

        # Buttons
        self.submit_button = QPushButton("Submit class")
        self.submit_button.setFixedSize(150, 40)
        layout.addWidget(self.submit_button, 4, 0)
        self.submit_button.clicked.connect(self.process_input)

        self.next_button = QPushButton("Next page")
        self.next_button.setFixedSize(150, 40)
        layout.addWidget(self.next_button, 4, 2)
        self.next_button.clicked.connect(self.close)

        self.setLayout(layout)
    
    def process_input(self):
        try:
            data = {
                'name': self.input_box1.text(),
                'days': self.input_box2.text().split(),
                'start': self.input_box3.text().split()[0].split('-')[0],
                'end': self.input_box3.text().split()[0].split('-')[1],
                'meridian': self.input_box3.text().split()[1],
                'difficulty': int(self.input_box4.text())
            }
            self.submitted.emit(data)
            
            # Clear inputs
            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()
            self.input_box4.clear()

        except Exception as e:
            print(f"Error: {e}")

class ActivityInputWindow(QWidget):
    submitted = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Activity Input")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QGridLayout()

        # Activity input
        self.label1 = QLabel('Activity: ')
        self.input_box1 = QLineEdit()
        self.input_box1.setMinimumWidth(300)
        layout.addWidget(self.label1, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box1, 0, 1)

        # Days input
        self.label2 = QLabel('Days (m, t, w, th, f): ')
        self.input_box2 = QLineEdit()
        layout.addWidget(self.label2, 1, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box2, 1, 1)

        # Time input
        self.label3 = QLabel('Time (start-finish AM/PM): ')
        self.input_box3 = QLineEdit()
        layout.addWidget(self.label3, 2, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box3, 2, 1)

        # Buttons
        self.submit_button = QPushButton("Submit activity")
        self.submit_button.setFixedSize(150, 40)
        layout.addWidget(self.submit_button, 3, 0)
        self.submit_button.clicked.connect(self.process_input)

        self.next_button = QPushButton("Next page")
        self.next_button.setFixedSize(150, 40)
        layout.addWidget(self.next_button, 3, 2)
        self.next_button.clicked.connect(self.close)

        self.setLayout(layout)
    
    def process_input(self):
        try:
            data = {
                'name': self.input_box1.text(),
                'days': self.input_box2.text().split(),
                'start': self.input_box3.text().split()[0].split('-')[0],
                'end': self.input_box3.text().split()[0].split('-')[1],
                'meridian': self.input_box3.text().split()[1]
            }
            self.submitted.emit(data)
            
            # Clear inputs
            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()

        except Exception as e:
            print(f"Error: {e}")

class PreferencesWindow(QWidget):
    submitted = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preferences")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QGridLayout()

        # Start time
        self.start_label = QLabel('Time willing to start: ')
        self.input_box1 = QLineEdit()
        self.input_box1.setMinimumWidth(300)
        layout.addWidget(self.start_label, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box1, 0, 1)

        # End time
        self.end_label = QLabel('Time willing to end: ')
        self.input_box2 = QLineEdit()
        layout.addWidget(self.end_label, 1, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box2, 1, 1)

        # Max hours
        self.max_label = QLabel('Max hours: ')
        self.input_box3 = QLineEdit()
        layout.addWidget(self.max_label, 2, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box3, 2, 1)

        # Min hours
        self.min_label = QLabel('Min hours: ')
        self.input_box4 = QLineEdit()
        layout.addWidget(self.min_label, 3, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_box4, 3, 1)

        # Buttons
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
            data = {
                'start_time': self.input_box1.text(),
                'end_time': self.input_box2.text(),
                'max_hours': int(self.input_box3.text()),
                'min_hours': int(self.input_box4.text())
            }
            self.submitted.emit(data)
            
            # Clear inputs
            self.input_box1.clear()
            self.input_box2.clear()
            self.input_box3.clear()
            self.input_box4.clear()

        except Exception as e:
            print(f"Error: {e}")
    
    def finish(self):
        self.close()

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
        table.setHorizontalHeaderLabels(['Day', 'Schedule', 'Classes', 'Activities', 'Study Times'])

        day_name_map = {
            'm': 'Monday',
            't': 'Tuesday',
            'w': 'Wednesday',
            'th': 'Thursday',
            'f': 'Friday',
            'sat': 'Saturday',
            'sun': 'Sunday'
        }

        for i, day in enumerate(self.schedule_data):
            full_day_name = day_name_map.get(day.name, day.name)
            item_day = QTableWidgetItem(full_day_name)
            
            # Add other columns similarly
            # Classes column
            if not day.courses:
                classes_str = 'No classes'
            else:
                classes_str = '\n'.join(f' {c.name} ({c.time_range()})' for c in day.courses)

            # Study Times column
            if not day.study_times:
                study_str = 'No study sessions'
            else:
                study_str = '\n'.join(f'{s.name} ({s.time_range()})' for s in day.study_times)

            # Activities column
            if not day.activities:
                activity_str = 'No activities'
            else:
                activity_str = '\n'.join(f'{a.name} ({a.time_range()})' for a in day.activities)

            # Combined Schedule column
            combined_list = self.schedule_data.get_sorted_daily_items(day.name.lower())
            if not combined_list:
                combined_list = ['No classes, activities, or study sessions']

            # Create items for each column
            item_schedule = QTableWidgetItem('\n'.join(combined_list))
            item_schedule.setTextAlignment(Qt.AlignTop)
            item_schedule.setFlags(item_schedule.flags() | Qt.ItemIsEditable)

            item_classes = QTableWidgetItem(classes_str)
            item_classes.setTextAlignment(Qt.AlignTop)
            item_classes.setFlags(item_classes.flags() | Qt.ItemIsEditable)

            item_activity = QTableWidgetItem(activity_str)
            item_activity.setTextAlignment(Qt.AlignTop)
            item_activity.setFlags(item_activity.flags() | Qt.ItemIsEditable)

            item_study = QTableWidgetItem(study_str)
            item_study.setTextAlignment(Qt.AlignTop)
            item_study.setFlags(item_study.flags() | Qt.ItemIsEditable)

            # Set items in table
            table.setItem(i, 0, item_day)
            table.setItem(i, 1, item_schedule)
            table.setItem(i, 2, item_classes)
            table.setItem(i, 3, item_activity)
            table.setItem(i, 4, item_study)

        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setWordWrap(True)
        table.resize(800, 600)
        
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = ScheduleManager()
        self.current_window = None
        self.setup_navigation()
    
    def setup_navigation(self):
        # Create windows
        self.class_window = ClassInputWindow()
        self.activity_window = ActivityInputWindow()
        self.prefs_window = PreferencesWindow()
        
        # Connect signals
        self.class_window.submitted.connect(self.manager.add_course)
        self.class_window.next_button.clicked.connect(self.show_activity_window)
        
        self.activity_window.submitted.connect(self.manager.add_activity)
        self.activity_window.next_button.clicked.connect(self.show_prefs_window)
        
        self.prefs_window.submitted.connect(self.manager.set_preferences)
        self.prefs_window.finish_button.clicked.connect(self.show_schedule)
        
        # Show first window
        self.show_class_window()
    
    def show_class_window(self):
        if self.current_window:
            self.current_window.close()
        self.class_window.show()
        self.current_window = self.class_window
    
    def show_activity_window(self):
        if self.current_window:
            self.current_window.close()
        self.activity_window.show()
        self.current_window = self.activity_window
    
    def show_prefs_window(self):
        if self.current_window:
            self.current_window.close()
        self.prefs_window.show()
        self.current_window = self.prefs_window
    
    def show_schedule(self):
        optimized = optimize_schedule(self.manager)
        if self.current_window:
            self.current_window.close()
        self.schedule_window = ScheduleDisplayWindow(optimized)
        self.schedule_window.show()
        self.current_window = self.schedule_window