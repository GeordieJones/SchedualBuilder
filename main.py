

class Course:
    def __init__(self, name, days, sameTime, start, end):
        self.name = name
        self.days = days
        self.sameTime = sameTime
        self.start = start
        self.end = end
    def __str__(self):
        return f"{self.name}:\n\tDays: {self.days}\n\tsame time? {self.sameTime}\n\tStart: {self.start}\n\tEnd: {self.end}\n\n"




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