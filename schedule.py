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


def get_event_window(time: str, duration: float) -> tuple[datetime, datetime]:
    start = datetime.strptime(time, "%H:%M")
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

    new_start, new_end = get_event_window(time, duration)

    for event in data["events"]:
        if event["date"] != date:
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