import main
import random

def time_to_minutes(time_str, period):
    if ":" not in time_str:
        time_str += ":00"  # auto-correct like "8" → "8:00"
    hours, minutes = map(int, time_str.split(":"))
    if period.lower() == "pm" and hours != 12:
        hours += 12
    if period.lower() == "am" and hours == 12:
        hours = 0
    return hours * 60 + minutes


def minutes_to_time(minutes):
    # FIX: Handle day overflow correctly
    minutes = int(round(minutes))
    if minutes >= 1440:  # 24 hours
        minutes = minutes % 1440
    
    hours = minutes // 60
    mins = minutes % 60
    if hours == 0:
        return f"12:{mins:02d} AM"
    elif hours < 12:
        return f"{hours}:{mins:02d} AM"
    elif hours == 12:
        return f"12:{mins:02d} PM"
    else:
        return f"{hours-12}:{mins:02d} PM"
TIME_BETWEEN = 5

def available_study_times(combined_list, vals):
    """Find all available time slots for studying (without applying daily max limit here)"""
    full_blocks = [[] for _ in range(7)]
    start_time = vals['start'][0]
    end_time = vals['end'][0]
    
    # If they're lists, take the first element
    if isinstance(start_time, list):
        start_time = start_time[0]
    if isinstance(end_time, list):
        end_time = end_time[0]
    
    start_day = time_to_minutes(start_time, "am")
    end_day = time_to_minutes(end_time, "pm")
    min_study = int((float(vals['min'])) * 60)

    for i, day in enumerate(combined_list):
        study_blocks = []
        open_start = start_day

        entries = sorted(day.courses + day.activities, key=lambda x: time_to_minutes(x.start, x.meridian))

        for entry in entries:
            try:
                start_min = time_to_minutes(entry.start, entry.meridian)
                end_min = time_to_minutes(entry.end, entry.meridian)
                
                # Check if there's a valid study block before this entry
                available_time = start_min - TIME_BETWEEN - open_start
                if available_time >= 20:  # minimum 20 minutes
                    study_blocks.append((minutes_to_time(open_start), minutes_to_time(start_min - TIME_BETWEEN)))
                
                open_start = end_min + TIME_BETWEEN
            except AttributeError:
                print(f"Skipping malformed entry on day {i}: {entry}")

        # Check for remaining time at end of day
        if open_start < end_day:
            remaining_time = end_day - open_start
            if remaining_time >= 30:  # minimum 30 minutes
                study_blocks.append((minutes_to_time(open_start), minutes_to_time(end_day)))

        full_blocks[i] = study_blocks
    return full_blocks

def calculate_total_study_time(free_time_slots):
    """Calculate total available study time in minutes"""
    total_time = 0
    for day_slots in free_time_slots:
        for start_str, end_str in day_slots:
            start_minutes = time_to_minutes(start_str.split()[0], start_str.split()[1])
            end_minutes = time_to_minutes(end_str.split()[0], end_str.split()[1])
            total_time += (end_minutes - start_minutes)
    return total_time

def optimize_times(combined_list, vals):
    """Optimize study time allocation based on course difficulty"""
    free_time_slots = available_study_times(combined_list, vals)
    
    all_courses = []
    seen_names = set()
    for day in combined_list:
        for course in day.courses:
            if course.name not in seen_names:
                all_courses.append(course)
                seen_names.add(course.name)
    
    courses_by_difficulty = sorted(all_courses, key=lambda c: c.difficulty, reverse=True)
    
    if not courses_by_difficulty:
        return []
    
    total_difficulty_weight = sum(course.difficulty for course in courses_by_difficulty)
    total_time = calculate_total_study_time(free_time_slots)
    
    optimal_times = []
    for course in courses_by_difficulty:
        proportion = course.difficulty / total_difficulty_weight
        study_time_for_course = total_time * proportion
        print(f"[optimize_times] Course '{course.name}': weekly study time = {study_time_for_course:.2f} minutes")
        
        optimal_times.append((course.name, study_time_for_course))
    
    return optimal_times

def schedule_study_sessions(combined_list,vals):
    free_time_slots = available_study_times(combined_list, vals)
    study_allocations = optimize_times(combined_list, vals)
    num_days = len(free_time_slots)
    max_daily_minutes = int(float(vals['max']) * 60)
    
    # Convert to dict for easier lookup
    course_weekly_times = dict(study_allocations)
    
    scheduled_sessions = []

    for day_index, day_slots in enumerate(free_time_slots):
        day_name = combined_list[day_index].name
        
        # Calculate daily targets (could be made more sophisticated)
        daily_targets = {course: weekly_time / num_days
                        for course, weekly_time in course_weekly_times.items()}
        
        day_sessions = schedule_daily(day_name, day_slots, daily_targets,max_daily_minutes)
        scheduled_sessions.extend(day_sessions)
    
    return scheduled_sessions



def schedule_daily(day_name, time_slots, course_targets, max_daily_minutes):
    sessions = []
    remaining = course_targets.copy()
    daily_time_used = 0

    for start_str, end_str in time_slots:
        if daily_time_used >= max_daily_minutes:
            break
        start_minutes = time_to_minutes(start_str.split()[0], start_str.split()[1])
        end_minutes = time_to_minutes(end_str.split()[0], end_str.split()[1])
        slot_duration = end_minutes - start_minutes

        available_time = min(slot_duration, max_daily_minutes - daily_time_used)
        if available_time < 30:  # minimum 30 min blocks
            continue
        
        current_start = start_minutes
        slot_remaining = available_time


        while slot_remaining >= 30 and remaining and daily_time_used < max_daily_minutes:
            best_course = find_best_course_for_slot(remaining, slot_remaining)
            
            if not best_course:
                break
                
            max_session_length = min(120, slot_remaining, max_daily_minutes - daily_time_used)
            study_duration = min(remaining[best_course], max_session_length)
            
            if study_duration < 30:
                break

            sessions.append({
                'course': best_course,
                'day': day_name,
                'start': minutes_to_time(current_start),
                'end': minutes_to_time(current_start + study_duration)
            })

            remaining[best_course] -= study_duration
            daily_time_used += study_duration
            current_start += study_duration
            slot_remaining -= study_duration
            
            if remaining[best_course] <= 0:
                del remaining[best_course]

    return sessions



def find_best_course_for_slot(targets, slot_duration):
    if slot_duration < 30:
        return None
    valid_courses = {course: time for course, time in targets.items() if time > 0}
    if not valid_courses:
        return None

    # Sort courses by remaining time descending
    sorted_courses = sorted(valid_courses.items(), key=lambda x: x[1], reverse=True)

    # Pick randomly from top N (e.g. top 3) to give smaller courses a chance
    top_n = min(3, len(sorted_courses))
    chosen_course = random.choice(sorted_courses[:top_n])[0]
    return chosen_course





def optimize(combined_list, vals):
    if not vals or 'start' not in vals or 'end' not in vals:
        print("Warning: Study time preferences not set. Using defaults.")
        # Use your add_values function structure
        vals = {}
        vals['start'] = ('8:00', 'AM')
        vals['end'] = ('10:00', 'PM')
        vals['max'] = 4.0  # 4 hours max per day
        vals['min'] = 1.0

    scheduled_sessions = schedule_study_sessions(combined_list, vals)

    for session in scheduled_sessions:
        # Extract meridian from time string
        start_parts = session['start'].split()
        end_parts = session['end'].split()
        
        main.add_study(
            session['course'],
            [session['day']],
            start_parts[0],  # time part
            end_parts[0],    # time part
            start_parts[1]   # meridian
        )
    


