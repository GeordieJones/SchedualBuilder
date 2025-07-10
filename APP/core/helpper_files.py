import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)
import windows.table_window as tb

'''
need to make one big class that hold the week with small functions
inside to be more concise
'''

# === Data Classes ===

all_courses = []
all_activities = []
all_studies = []


class Course:
    def __init__(self, name, days, start, end, meridian, difficulty):
        self.name = name
        self.days = days
        self.start = self.normalize_time(start)
        self.end = self.normalize_time(end)
        self.meridian = meridian
        self.difficulty = difficulty

    def time_range(self):
        return f"{self.start}–{self.end} {self.meridian}"

    def normalize_time(self, t):
        """Converts '9' to '9:00' and ensures all times are in 'H:MM' format."""
        if ':' not in t:
            return f"{int(t)}:00"
        parts = t.split(':')
        if len(parts) == 2:
            hour = int(parts[0])
            minute = parts[1].zfill(2)
            return f"{hour}:{minute}"
        raise ValueError(f"Invalid time format: {t}")
    
    def sort_key(self):
        hour, minute = map(int, self.start.split(":"))
        if self.meridian == 'PM' and hour != 12:
            hour += 12
        if self.meridian == 'AM' and hour == 12:
            hour = 0
        return hour * 60 + minute


    def __str__(self):
        return f"{self.name}:\n\tDays: {self.days}\n\tStart: {self.start}\n\tEnd: {self.end}\n\t{self.meridian}\n\tDifficulty: {self.difficulty}\n"


class Day:
    days_of_week = ['m', 't', 'w', 'th', 'f', 'sat', 'sun']

    def __init__(self, name):
        self.name = name
        self.courses = []
        self.study_times = []
        self.activities = []

    def add_course(self, course):
        self.courses.append(course)
        self.courses.sort(key=lambda c: c.sort_key())
    
    def add_study_time(self, time_desc):
        self.study_times.append(time_desc)

    def add_activity(self, activity):
        self.activities.append(activity)
        self.activities.sort(key=lambda c: c.sort_key())

    def __str__(self):
        if not self.courses and not self.study_times:
            return f"{self.name}: No classes or study sessions\n"
        ret = f"{self.name}:\n"
        for course in self.courses:
            ret += f"  {course.name} ({course.start}–{course.end} {course.meridian})\n"
        for study in self.study_times:
            ret += f"  {study.name} ({study.time_range()})\n"
        return ret

class Activity:
    def __init__(self, name, days, start, end, meridian):
        self.name = name
        self.days = days
        self.start = self.normalize_time(start)
        self.end = self.normalize_time(end)
        self.meridian = meridian

    def time_range(self):
        return f"{self.start}–{self.end} {self.meridian}"

    def normalize_time(self, t):
        """Converts '9' to '9:00' and ensures all times are in 'H:MM' format."""
        if ':' not in t:
            return f"{int(t)}:00"
        parts = t.split(':')
        if len(parts) == 2:
            hour = int(parts[0])
            minute = parts[1].zfill(2)
            return f"{hour}:{minute}"
        raise ValueError(f"Invalid time format: {t}")
    
    def sort_key(self):
        hour, minute = map(int, self.start.split(":"))
        if self.meridian == 'PM' and hour != 12:
            hour += 12
        if self.meridian == 'AM' and hour == 12:
            hour = 0
        return hour * 60 + minute


    def __str__(self):
        return f"{self.name}:\n\tDays: {self.days}\n\tStart: {self.start}\n\tEnd: {self.end}\n\t{self.meridian}\n\n"

class Study:
    def __init__(self, name, days, start, end, meridian):
        self.name = name
        self.days = days
        self.start = self.normalize_time(start)
        self.end = self.normalize_time(end)
        self.meridian = meridian

    def time_range(self):
        return f"{self.start}–{self.end} {self.meridian}"

    def normalize_time(self, t):
        """Converts '9' to '9:00' and ensures all times are in 'H:MM' format."""
        if ':' not in t:
            return f"{int(t)}:00"
        parts = t.split(':')
        if len(parts) == 2:
            hour = int(parts[0])
            minute = parts[1].zfill(2)
            return f"{hour}:{minute}"
        raise ValueError(f"Invalid time format: {t}")
    
    def sort_key(self):
        hour, minute = map(int, self.start.split(":"))
        if self.meridian == 'PM' and hour != 12:
            hour += 12
        if self.meridian == 'AM' and hour == 12:
            hour = 0
        return hour * 60 + minute
    def __str__(self):
        return f"{self.name} ({self.time_range()})"




# === Core Logic Functions ===

class_days = [Day(day) for day in Day.days_of_week]

def get_all_sorted_items(day):
    items = []

    # Wrap all items with common structure
    for course in day.courses:
        items.append((course.sort_key(), f'Class: {course.name} ({course.time_range()})'))

    for activity in day.activities:
        items.append((activity.sort_key(), f'Activity: {activity.name} ({activity.time_range()})'))

    for study in day.study_times:
        items.append((study.sort_key(), f'Study: {study.name} ({study.time_range()})'))


    # Sort by time
    items.sort(key=lambda x: x[0])
    return [item[1] for item in items]



def convert_to_days(all_courses):
    """Converts a list of Course objects into Day objects."""
    #day_names = ['m', 't', 'w', 'th', 'f', 'sat', 'sun']
    day_names = Day.days_of_week
    week = {day: Day(day) for day in day_names}

    for course in all_courses:
        for d in course.days:
            if d in week:
                week[d].add_course(course)

    return [week[day] for day in day_names]



def add_class(name, days, start, end, meridian, difficulty):
    global all_courses
    course = Course(name, days, start, end, meridian, difficulty)
    all_courses.append(course)
    for d in days:
        for day_obj in class_days:
            if day_obj.name == d:
                day_obj.add_course(course)

def add_activity(name, days, start, end, meridian):
    global all_activities
    activity = Activity(name, days, start, end, meridian)
    all_activities.append(activity)
    for d in days:
        for day_obj in class_days:
            if day_obj.name == d:
                day_obj.add_activity(activity)

def add_study(name, days, start, end, meridian):
    global all_studies
    study = Study(name, days, start, end, meridian)
    all_studies.append(study)
    for d in days:
        for day_obj in class_days:
            if day_obj.name == d:
                day_obj.add_study_time(study)
                print(f"Added study session: {name} on {days} from {start} to {end} {meridian}")


vals = {}
def add_values(start_time, end_time, max_val, min_val):
    start = extract_time_part(start_time)
    end = extract_time_part(end_time)
    start_mardian = extract_meridian(start_time)
    end_mardian = extract_meridian(end_time)
    vals['start'] = (start, start_mardian)
    vals['end'] = (end, end_mardian)
    vals['max'] = max_val
    vals['min'] = min_val

def extract_meridian(time_str):
    return time_str.split(" ")[-1]

def extract_time_part(time_str):
    return time_str.strip().split(" ")[0]

def link_table():
    global class_days, vals
    return tb.show_data(class_days,vals)