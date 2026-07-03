import json 
from datetime import datetime, timedelta

def load_db(filename):
    with open(filename) as file:
        data = json.load(file)
    return data 

def save_db(filename, data):
    with open(filename,"w") as file:
        json.dump(data, file)

def add_task(filename, name, deadline, priority):
    data = load_db(filename)

    data["tasks"].append({"name":name,"deadline":deadline,"priority":priority})

    save_db(filename,data)

def add_event(filename,name, date, time, duration):
    data = load_db(filename)

    data["events"].append({"name":name,"date":date,"time":time,"duration":duration})

    save_db(filename,data)

def read_calendar(filename):
    data = load_db(filename)
    return data["events"]

def list_tasks(filename):
    data = load_db(filename)
    return data["tasks"]

def find_free_slots(filename, duration, day_start, day_end):
    data = load_db(filename)
    events = data["events"]
    events = sorted(events, key=lambda event: datetime.strptime(event["time"], "%H:%M"))

    day_start = datetime.strptime(day_start, "%H:%M")
    day_end = datetime.strptime(day_end, "%H:%M")
    duration = timedelta(hours=duration)

    free_slots = []
    current_time = day_start

    for event in events:
        event_start = datetime.strptime(event["time"], "%H:%M")
        event_end = event_start + timedelta(hours=event["duration"])
        
        if event_start - current_time >= duration:
            free_slots.append((current_time.strftime("%H:%M"),event_start.strftime("%H:%M")))

        current_time = max(current_time, event_end)
        
    if day_end - current_time >= duration:
        free_slots.append((current_time.strftime("%H:%M"), day_end.strftime("%H:%M")))

    return free_slots