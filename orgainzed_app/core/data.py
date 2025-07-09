from .models import Course, Activity, StudySession, DaySchedule, TimeSlot
from typing import Dict, List

class ScheduleManager:
    def __init__(self):
        self.courses: List[Course] = []
        self.activities: List[Activity] = []
        self.study_sessions: List[StudySession] = []
        self._day_schedules = None
        
    @property
    def day_schedules(self) -> Dict[str, DaySchedule]:
        """Dynamically generates the combined schedule when accessed"""
        if self._day_schedules is None:
            self._rebuild_schedules()
        return self._day_schedules
    
    def _rebuild_schedules(self):
            """Rebuilds the entire schedule structure with proper sorting"""
            schedules = {
                day: DaySchedule(day, [], [], []) 
                for day in ['m', 't', 'w', 'th', 'f', 'sat', 'sun']
            }
            # Populate from all sources
            for course in self.courses:
                for day in course.days:
                    if day in schedules:
                        schedules[day].courses.append(course)
            
            for activity in self.activities:
                for day in activity.days:
                    if day in schedules:
                        schedules[day].activities.append(activity)
            
            for study in self.study_sessions:
                if study.day in schedules:
                    schedules[study.day].study_sessions.append(study)
            
            # Sort each day's items once
            for day_schedule in schedules.values():
                day_schedule.courses.sort(key=lambda x: x.time.to_minutes())
                day_schedule.activities.sort(key=lambda x: x.time.to_minutes())
                day_schedule.study_sessions.sort(key=lambda x: x.time.to_minutes())
            
            self._day_schedules = schedules

    def _invalidate_cache(self):
        """Marks schedules as needing rebuild"""
        self._day_schedules = None


    def add_course(self, course_data: dict):
        time_slot = TimeSlot(
            start=course_data['start'],
            end=course_data['end'],
            meridian=course_data['meridian']
        )
        self.courses.append(Course(
            name=course_data['name'],
            days=course_data['days'],
            time=time_slot,
            difficulty=course_data['difficulty']
        ))
        self._invalidate_cache()

    def add_activity(self, activity_data: dict):
        time_slot = TimeSlot(
            start=activity_data['start'],
            end=activity_data['end'],
            meridian=activity_data['meridian']
        )
        self.activities.append(Activity(
            name=activity_data['name'],
            days=activity_data['days'],
            time=time_slot,
        ))
        self._invalidate_cache()

    def add_study(self, study_data: dict):
        time_slot = TimeSlot(
            start=study_data['start'],
            end=study_data['end'],
            meridian=study_data['meridian']
        )
        self.study_sessions.append(StudySession(
            course_name=study_data['name'],
            days=study_data['days'][0],
            time=time_slot,
        ))
        self._invalidate_cache()

    def get_sorted_daily_items(self, day: str) -> List[str]:
        """Returns formatted strings of all items in chronological order"""
        day_schedule = self.day_schedules.get(day)
        if not day_schedule:
            return []
            
        # Combine all items with their timestamps
        all_items = []
        all_items.extend((c.time.to_minutes(), f'Class: {c.name} ({c.time.start}-{c.time.end} {c.time.meridian})') 
                        for c in day_schedule.courses)
        all_items.extend((a.time.to_minutes(), f'Activity: {a.name} ({a.time.start}-{a.time.end} {a.time.meridian})') 
                        for a in day_schedule.activities)
        all_items.extend((s.time.to_minutes(), f'Study: {s.course_name} ({s.time.start}-{s.time.end} {s.time.meridian})') 
                        for s in day_schedule.study_sessions)
        
        # Return sorted by time
        return [item[1] for item in sorted(all_items, key=lambda x: x[0])]
