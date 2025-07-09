from .models import Course, Activity, StudySession, DaySchedule, TimeSlot
from typing import List

class ScheduleManager:
    def __init__(self):
        self.courses: List[Course] = []
        self.activities: List[Activity] = []
        self.study_sessions: List[StudySession] = []
        self.day_schedules = {
            day: DaySchedule(day, [], [], []) 
            for day in ['m', 't', 'w', 'th', 'f', 'sat', 'sun']
        }
    
    def add_course(self, course_data: dict):
        time_slot = TimeSlot(
            start=course_data['start'],
            end=course_data['end'],
            meridian=course_data['meridian']
        )
        course = Course(
            name=course_data['name'],
            days=course_data['days'],
            time=time_slot,
            difficulty=course_data['difficulty']
        )
        self.courses.append(course)
        self._update_day_schedules()
    
    def _update_day_schedules(self):
        # Update day_schedules with current courses/activities
        pass
    
    # Similar methods for activities, study sessions, etc.