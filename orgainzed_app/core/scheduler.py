from .models import ScheduleManager, TimeSlot
from .logic import schedule_study_sessions

def optimize_schedule(manager: ScheduleManager, preferences: dict = None):
    """Main optimization function that generates study sessions"""
    # 1. Prepare preferences with defaults if not provided
    vals = preferences or {
        'start': ('8:00', 'AM'),
        'end': ('10:00', 'PM'),
        'max': 4.0,  # hours
        'min': 1.0    # hours
    }

    # 2. Get current schedule data from manager
    combined_list = list(manager.day_schedules.values())  # Get all DaySchedule objects
    
    # 3. Generate optimal study sessions
    scheduled_sessions = schedule_study_sessions(combined_list, vals)
    
    # 4. Add sessions to ScheduleManager
    for session in scheduled_sessions:
        # Parse time components
        start_time, start_meridian = session['start'].rsplit(' ', 1)
        end_time, end_meridian = session['end'].rsplit(' ', 1)
        
        # Ensure meridian matches for both times
        meridian = start_meridian  # Use start time's meridian
        
        manager.add_study({
            'name': f"Study for {session['course']}",
            'days': [session['day']],
            'start': start_time,
            'end': end_time,
            'meridian': meridian
        })
    
    # 5. Return the updated manager with new study sessions
    return manager