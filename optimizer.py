

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
    hours = minutes // 60
    mins = minutes % 60
    suffix = "AM" if hours < 12 or hours == 24 else "PM"
    if hours > 12:
        hours -= 12
    if hours == 0:
        hours = 12
    return f"{hours}:{mins:02d} {suffix}"

TIME_BETWEEN = 5

def optimize(combined_list, vals):
    full_blocks = [[]for _ in range(7)]
    start_day = time_to_minutes(vals['start'][0], "am")
    end_day = time_to_minutes(vals['end'][0], "pm")
    max_study = int((float(vals['max_val'][0])) *60)
    min_study = int((float(vals['min_val'][0])) *60)

    for i, day in enumerate(combined_list):
        study_blocks = []
        time_studied = 0
        open_start = start_day

        entries = sorted(day.courses + day.activities, key=lambda x: time_to_minutes(x.start, x.meridian))


        for entry in entries:
            if(time_studied < max_study and open_start < end_day - 30):
                try:
                    start_min = time_to_minutes(entry.start, entry.meridian)
                    end_min = time_to_minutes(entry.end, entry.meridian)
                    if((start_min - open_start) >= 20 and time_studied < max_study):
                        time_studied += ((start_min-TIME_BETWEEN) - open_start)
                        study_blocks.append((open_start, start_min-TIME_BETWEEN))
                        open_start = end_min + TIME_BETWEEN
                    else:
                        open_start = end_min + TIME_BETWEEN
                except AttributeError:
                    print(f"Skipping malformed entry on day {i}: {entry}")

        if open_start < end_day:
            remaining_time = end_day - open_start
            if time_studied < max_study and remaining_time >= 30:
                if time_studied + remaining_time < max_study:
                    study_blocks.append((open_start, end_day))
                else:
                    block_end = open_start + (max_study - time_studied)
                    study_blocks.append((open_start, block_end))

        full_blocks[i] = study_blocks
    return full_blocks
