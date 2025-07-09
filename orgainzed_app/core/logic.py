from .models import DaySchedule

def normalize_time(time_str: str) -> str:
    """Convert time strings to consistent format"""
    if ':' not in time_str:
        return f"{time_str}:00"
    return time_str

def get_all_sorted_items(day_schedule: DaySchedule) -> List[str]:
    """Combine and sort all schedule items for a day"""
    all_items = []
    # Combine courses, activities, study sessions
    # Sort by time
    return sorted_items

def time_to_minutes(time_str: str, period: str) -> int:
    """Convert time string to minutes since midnight"""
    # Implementation
    pass