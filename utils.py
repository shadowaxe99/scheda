
import datetime

def get_current_time():
    return datetime.datetime.now()

def calculate_duration(start_time, end_time):
    duration = end_time - start_time
    return duration

def format_time(time):
    return time.strftime("%H:%M")

def get_weekday(date):
    return date.strftime("%A")

def is_weekend(date):
    weekday = get_weekday(date)
    if weekday == "Saturday" or weekday == "Sunday":
        return True
    return False

