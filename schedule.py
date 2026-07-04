import json 
from datetime import datetime, timedelta

DB_FILE = "schedule.json"


def load_db(filename):
    with open(filename) as file:
        data = json.load(file)
    return data 


def save_db(filename, data):
    with open(filename,"w") as file:
        json.dump(data, file, indent=2)


def normalize_date(date: str) -> str:
    return datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")


def normalize_time(time: str) -> str:
    return datetime.strptime(time, "%H:%M").strftime("%H:%M")


def get_event_window(time: str, duration: float) -> tuple[datetime, datetime]:
    start = datetime.strptime(normalize_time(time), "%H:%M")
    end = start + timedelta(hours=duration)
    return start, end


def events_overlap(
    first_start: datetime,
    first_end: datetime,
    second_start: datetime,
    second_end: datetime,
) -> bool:
    return first_start < second_end and second_start < first_end


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

    deadline = normalize_date(deadline)

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

    date = normalize_date(date)
    time = normalize_time(time)
    new_start, new_end = get_event_window(time, duration)

    for event in data["events"]:
        if normalize_date(event["date"]) != date:
            continue

        event_start, event_end = get_event_window(event["time"], event["duration"])
        if events_overlap(new_start, new_end, event_start, event_end):
            raise ValueError(
                f"Cannot add '{name}' because it overlaps with "
                f"'{event['name']}' from {event_start.strftime('%H:%M')} "
                f"to {event_end.strftime('%H:%M')} on {date}."
            )

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
    date: str,
    duration: float,
    day_start: str,
    day_end: str,
) -> list[tuple[str, str]]:
    """
    Find all available time slots within a day that can fit a given duration.

    Args:
        date: Date to check in YYYY-MM-DD format.
        duration: Required duration in hours.
        day_start: Beginning of the scheduling window in HH:MM format.
        day_end: End of the scheduling window in HH:MM format.

    Returns:
        A list of tuples containing the start and end time of each free slot.
        Example:
            [("08:00", "10:30"), ("14:00", "17:00")]
    """
    data = load_db(DB_FILE)
    date = normalize_date(date)
    events = [
        event
        for event in data["events"]
        if normalize_date(event["date"]) == date
    ]
    events = sorted(events, key=lambda event: normalize_time(event["time"]))

    day_start = datetime.strptime(normalize_time(day_start), "%H:%M")
    day_end = datetime.strptime(normalize_time(day_end), "%H:%M")
    duration = timedelta(hours=duration)

    free_slots = []
    current_time = day_start

    for event in events:
        event_start, event_end = get_event_window(event["time"], event["duration"])
        
        if event_start - current_time >= duration:
            free_slots.append((current_time.strftime("%H:%M"),event_start.strftime("%H:%M")))

        current_time = max(current_time, event_end)
        
    if day_end - current_time >= duration:
        free_slots.append((current_time.strftime("%H:%M"), day_end.strftime("%H:%M")))

    return free_slots
