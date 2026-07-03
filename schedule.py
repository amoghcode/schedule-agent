import json 
from datetime import datetime, timedelta

DB_FILE = "schedule.json"
def load_db(filename):
    with open(filename) as file:
        data = json.load(file)
    return data 

def save_db(filename, data):
    with open(filename,"w") as file:
        json.dump(data, file)

def add_task(
    name: str,
    deadline: str,
    priority: str,
) -> None:
    """
    Add a new task to the scheduler.

    Args:
        name: Name or description of the task.
        deadline: Deadline in YYYY-MM-DD format.
        priority: Priority level of the task.

    Returns:
        None
    """
    data = load_db(DB_FILE)

    data["tasks"].append({"name":name,"deadline":deadline,"priority":priority})

    save_db(DB_FILE,data)

def add_event(
    name: str,
    date: str,
    time: str,
    duration: float,
) -> None:
    """
    Add a new event to the calendar.

    Args:
        name: Name of the event.
        date: Event date in YYYY-MM-DD format.
        time: Event start time in HH:MM (24-hour) format.
        duration: Duration of the event in hours.

    Returns:
        None
    """
    data = load_db(DB_FILE)

    data["events"].append({"name":name,"date":date,"time":time,"duration":duration})

    save_db(DB_FILE,data)

def read_calendar() -> list[dict]:
    """
    Retrieve all scheduled calendar events.

    Returns:
        A list of dictionaries representing calendar events.
    """
    data = load_db(DB_FILE)
    return data["events"]


def list_tasks() -> list[dict]:
    """
    Retrieve all scheduled tasks.

    Returns:
        A list of dictionaries representing tasks.
    """
    data = load_db(DB_FILE)
    return data["tasks"]

def find_free_slots(
    duration: float,
    day_start: str,
    day_end: str,
) -> list[tuple[str, str]]:
    """
    Find all available time slots within a day that can fit a given duration.

    Args:
        duration: Required duration in hours.
        day_start: Beginning of the scheduling window in HH:MM format.
        day_end: End of the scheduling window in HH:MM format.

    Returns:
        A list of tuples containing the start and end time of each free slot.
        Example:
            [("08:00", "10:30"), ("14:00", "17:00")]
    """
    data = load_db(DB_FILE)
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