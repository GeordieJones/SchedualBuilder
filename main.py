import tkinter as tk
from tkinter import simpledialog, messagebox

class Course:
    def __init__(self, name, days, sameTime, start, end):
        self.name = name
        self.days = days
        self.sameTime = sameTime
        self.start = start
        self.end = end
    def __str__(self):
        return f"{self.name}:\n\tDays: {self.days}\n\tsame time? {self.sameTime}\n\tStart: {self.start}\n\tEnd: {self.end}\n\n"

class Day:
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



inputed_classes = input('Classes:')
classes = inputed_classes.split()
all_course = []
for i in range(len(classes)):
    day = input(f'what day do you have {classes[i]}: ')
    days = day.split()
    sameTime = bool(input('is this class at the same time each day: '))
    start = input('when does this class start: ')
    end  = input('what does this class end: ')
    c1 = Course(classes[i], days, sameTime, start, end)
    all_course.append(c1)


for i in all_course:
    for course in all_course:
        print(course)