import tkinter as tk
from tkinter import simpledialog, messagebox

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

class Course:
    def __init__(self, name, days, sameTime, start, end):
        self.name = name
        self.days = days
        self.sameTime = sameTime
        self.start = start
        self.end = end
    def __str__(self):
        return (f"{self.name}:\n"
                f"\tDays: {self.days}\n"
                f"\tsame time? {self.sameTime}\n"
                f"\tStart: {self.start}\n"
                f"\tEnd: {self.end}\n")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule Builder")
        
        self.courses = []
        
        # Input field for class names
        self.label = tk.Label(root, text="Enter classes (space separated):")
        self.label.pack()
        
        self.class_entry = tk.Entry(root, width=50)
        self.class_entry.pack()
        
        self.add_button = tk.Button(root, text="Add Classes", command=self.add_classes)
        self.add_button.pack()
        
        self.output_text = tk.Text(root, height=15, width=60)
        self.output_text.pack()
        
    def add_classes(self):
        inputed_classes = self.class_entry.get()
        classes = inputed_classes.split()
        
        if not classes:
            messagebox.showwarning("Input Error", "Please enter at least one class name.")
            return
        
        for class_name in classes:
            day = simpledialog.askstring("Days", f"What days do you have {class_name}? (space separated)")
            if day is None:
                continue
            days = day.split()
            # create a class for each day
            
            
            sameTime_input = simpledialog.askstring("Same Time?", f"Is {class_name} at the same time each day? (yes/no)")
            if sameTime_input is None:
                continue
            sameTime = sameTime_input.strip().lower() == "yes"
            # add a function if no how many differnt times and what are the new times
            if sameTime != 'yes':
                numoftimes = simpledialog.askstring("number of different Times", f"What times?")
            start = simpledialog.askstring("Start Time", f"When does {class_name} start?")
            if start is None:
                continue
            
            end = simpledialog.askstring("End Time", f"When does {class_name} end?")
            if end is None:
                continue
            
            course = Course(class_name, days, sameTime, start, end)
            self.courses.append(course)
        
        self.show_courses()
    
    def show_courses(self):
        self.output_text.delete('1.0', tk.END)
        for course in self.courses:
            self.output_text.insert(tk.END, str(course) + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
