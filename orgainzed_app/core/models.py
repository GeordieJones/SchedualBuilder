from dataclasses import dataclass
from typing import List

@dataclass
class TimeSlot:
    start: str
    end: str
    meridian: str
    
    def to_minutes(self):
        time_str = self.start  # or self.end depending on what you need
        if ":" not in time_str:
            time_str += ":00"
        hours, minutes = map(int, time_str.split(":"))
        if self.meridian.lower() == "pm" and hours != 12:
            hours += 12
        if self.meridian.lower() == "am" and hours == 12:
            hours = 0
        return hours * 60 + minutes

@dataclass
class Course:
    name: str
    days: List[str]
    time: TimeSlot
    difficulty: int
    #assignments: List['Assignment'] = None
    #exams: List['Exam'] = None

@dataclass 
class Activity:
    name: str
    days: List[str]
    time: TimeSlot

@dataclass
class StudySession:
    course_name: str
    day: str
    time: TimeSlot

@dataclass
class DaySchedule:
    day: str
    courses: List[Course]
    activities: List[Activity]
    study_sessions: List[StudySession]