import tkinter as tk
from tkinter import simpledialog, messagebox

class Course:
    def __init__(self, name, days, start, end):
        self.name = name
        self.days = days
        self.start = start
        self.end = end
    def __str__(self):
        return f"{self.name}:\n\tDays: {self.days}\n\tStart: {self.start}\n\tEnd: {self.end}\n\n"

class Day:
    days_of_week = ['m', 't', 'w', 'th', 'f', 'sat','san']
    def __init__(self,name, day, start, end):
        self.name = name
        self.day = day
        self.start = start
        self.end = end
    def __str__(self):
        times = ['8','9','10','11','12','1','2','3','4','5']
        ret = ''
        for i in times:
            if int(times[i]) == self.start or int(times[i]) == self.end:
                ret+= f"{times[i]}: {self.name}\n"
            else:
                ret += f"{times[i]}\n"
        return (f"{self.day}:\n {ret}")

def convert_to_days(course):
    name = course.name
    days = course.days
    start = course.start
    end = course.end
    # need to change this to add courses to the given days


inputed_classes = input('Classes:')
classes = inputed_classes.split()
all_course = []
for i in range(len(classes)):
    day = input(f'what days do you have {classes[i]}: ')
    days = day.split()
    sameTime = (input('is this class at the same time each day: ').strip().lower() == 'yes')
    if not sameTime:
        numOfTimes = int(input('how many differnt times: '))
        for times in range(numOfTimes+1):
            start = input(f'when does this class start: ')
            end  = input(f'when does this class end: ')
            same = input('what days have this time: ').split()
            c1  = Course(classes[i],same, start, end)
            all_course.append(c1)
        continue
    start = input('when does this class start: ')
    end  = input('what does this class end: ')
    c1 = Course(classes[i], days, start, end)
    all_course.append(c1)

for course in all_course:
    convert_to_days(all_course[course])


for course in all_course:
    print(course)