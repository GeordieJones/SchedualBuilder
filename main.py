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

class Course:
    def __init__(self, name, days, start, end, meridian):
        self.name = name
        self.days = days
        self.start = start
        self.end = end
        self.meridian = meridian

    def time_range(self):
        return f"{self.start}–{self.end} {self.meridian}"
    
    def sort_key(self):
        hour, minute = map(int, self.start.split(":"))
        if self.meridian == 'PM' and hour != 12:
            hour += 12
        if self.meridian == 'AM' and hour == 12:
            hour = 0
        return hour * 60 + minute


    def __str__(self):
        return f"{self.name}:\n\tDays: {self.days}\n\tStart: {self.start}\n\tEnd: {self.end}\n\t{self.meridian}\n"


class Day:
    days_of_week = ['m', 't', 'w', 'th', 'f', 'sat', 'sun']

    def __init__(self, name):
        self.name = name
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)
        self.courses.sort(key=lambda c: c.sort_key())

    def __str__(self):
        if not self.courses:
            return f"{self.name}: No classes\n"
        ret = f"{self.name}:\n"
        for course in self.courses:
            ret += f"  {course.name} ({course.start}–{course.end}{course.meridian})\n"
        return ret


# === Core Logic Functions ===

def get_classes():
    """Gathers user input and returns a list of Course objects."""
    inputed_classes = input('Enter class names (space-separated): ')
    class_names = inputed_classes.split()
    all_courses = []

    for name in class_names:
        day_input = input(f'What days do you have {name}? ').lower()
        days = day_input.split()
        same_time = input('Is this class at the same time each day? (yes/no): ').strip().lower() == 'yes'

        if not same_time:
            num_times = int(input('How many different times? '))
            for _ in range(num_times):
                start = input(f'When does this class start? ')
                end = input(f'When does this class end? ')
                meridian = input(f'AM or PM? ').upper()
                specific_days = input('What days have this time? ').lower().split()
                all_courses.append(Course(name, specific_days, start, end, meridian))
        else:
            start = input('When does this class start? ')
            end = input('When does this class end? ')
            meridian = input(f'AM or PM? ').upper()
            all_courses.append(Course(name, days, start, end, meridian))

    return all_courses


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


def show_data(class_days):
    app = QApplication([])
    table = QTableWidget()
    table.setRowCount(len(class_days))
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(['Day', 'Schedule'])

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
            class_str = 'No classes'
        else:
            class_str = '\n'.join([f'{course.name} ({course.time_range()})'for course in day.courses])
        
        item_classes = QTableWidgetItem(class_str)
        item_classes.setTextAlignment(Qt.AlignTop)
        item_classes.setFlags(item_classes.flags() | Qt.ItemIsEditable)

        table.setItem(i, 0, item_day)
        table.setItem(i, 1, item_classes)
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.setWordWrap(True)
    table.setWindowTitle('Weekly Class Schedule')
    table.show()
    sys.exit(app.exec())

# === Main Entry Point ===

def main():
    all_courses = get_classes()

    print("\n--- Courses Entered ---")
    for course in all_courses:
        print(course)

    class_days = convert_to_days(all_courses)

    show_data(class_days)


if __name__ == "__main__":
    main()
