"""
Description:
This is the workhorse behind the calendar program.
It takes input and organizes it into Course and Day objects.

TO DO:
* Create a UI interface in a separate file to run this.
* Create an optimizer for study times.
* Add a class difficulty rating.
* Make it a list for a day like the calendar app.
* Add times to work in free time and other activities.
* Use marginal benefit and cost analysis.
"""
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)

# === Data Classes ===

all_courses = []
all_activities = []


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
            ret += f"  Study: {study}\n"
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




# === Core Logic Functions ===

class_days = [Day(day) for day in Day.days_of_week]

def get_all_sorted_items(day):
    items = []

    # Wrap all items with common structure
    for course in day.courses:
        items.append((course.sort_key(), f'{course.name} ({course.time_range()})'))

    for activity in day.activities:
        items.append((activity.sort_key(), f'Activity: {activity.name} ({activity.time_range()})'))

    for study_str in day.study_times:
        # Attempt to extract sort key from study_str like '2:00–3:00 PM'
        try:
            time_part, meridian = study_str.split(" ")
            start_time = time_part.split("–")[0]
            hour, minute = map(int, start_time.split(":"))
            if meridian == 'PM' and hour != 12:
                hour += 12
            if meridian == 'AM' and hour == 12:
                hour = 0
            key = hour * 60 + minute
        except:
            key = 9999  # Fallback sort key if format is wrong
        items.append((key, f'Study: {study_str}'))

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


def ask_day(class_days):
    """Asks for a day and prints the schedule for that day."""
    requested_day = input("Which day do you want to see classes for (m, t, w, th, f, sat, sun)? ").strip().lower()
    week_schedule = {day.name: day for day in class_days}

    if requested_day in week_schedule:
        print(week_schedule[requested_day])
    else:
        print("Invalid day. Try m, t, w, th, or f.")


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



def show_data(class_days):
    #app = QApplication([])
    table = QTableWidget()
    table.setRowCount(len(class_days))
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(['Day', 'Schedule', 'Classes', 'Activities','Study Times'])

    day_name_map = {
        'm': 'Monday',
        't': 'Tuesday',
        'w': 'Wednesday',
        'th': 'Thursday',
        'f': 'Friday',
        'sat': 'Saturday',
        'sun': 'Sunday'
    }

    for i, day in enumerate(class_days):
        full_day_name = day_name_map.get(day.name, day.name)
        item_day = QTableWidgetItem(full_day_name)

        if not day.courses:
            classes_str = 'No classes'
        else:
            classes_str = '\n'.join(f'{c.name} ({c.time_range()})' for c in day.courses)


        # Build study times string
        if not day.study_times:
            study_str = 'No study sessions'
        else:
            study_str = '\n'.join(day.study_times)

        if not day.activities:
            activity_str = 'No activities'
        else:
            activity_str = '\n'.join(f'Activity: {a.name} ({a.time_range()})' for a in day.activities)


            #before was activity_str = '\n'.join(day.study_times)


        # Build combined schedule string

        combined_list = get_all_sorted_items(day)
        if not combined_list:
            combined_list = ['No classes, activities, or study sessions']
        



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

        table.setItem(i, 0, item_day)
        table.setItem(i, 1, item_schedule)
        table.setItem(i, 2, item_classes)
        table.setItem(i, 3, item_activity)
        table.setItem(i, 4, item_study)
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.setWordWrap(True)
    table.resize(800, 600)
    for row in range(table.rowCount()):
        if table.rowHeight(row) < 50:
            table.setRowHeight(row, 50)
    table.setWindowTitle('Weekly Class Schedule')
    table.show()
    return table

def add_demo_study_times(class_days):
    # Just an example: add some study times per day
    for day in class_days:
        if day.name == 'm':
            day.add_study_time("2:00–3:00 PM")
        if day.name == 'w':
            day.add_study_time("5:00–6:30 PM")

# === Main Entry Point ===

def main():
    global class_days
    add_demo_study_times(class_days)
    show_data(class_days)



if __name__ == "__main__":
    main()
