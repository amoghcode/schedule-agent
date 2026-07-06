import json
import tempfile

import schedule


demo_data = {
    "tasks": [],
    "events": [
        {
            "name": "Morning class",
            "date": "2026-07-05",
            "time": "09:00",
            "duration": 1,
        },
        {
            "name": "Project meeting",
            "date": "2026-07-05",
            "time": "14:00",
            "duration": 1,
        },
    ],
}

with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as file:
    json.dump(demo_data, file, indent=2)
    schedule.DB_FILE = file.name

print("Initial calendar:")
print(json.dumps(schedule.read_calendar(), indent=2))

print("\nFree slots on 2026-07-05 for a 1-hour task:")
print(schedule.find_free_slots("2026-07-05", 1, "09:00", "17:00"))

print("\nAdding a new study session at 10:00...")
schedule.add_event("Study session", "2026-07-05", "10:00", 1)
print(json.dumps(schedule.read_calendar(), indent=2))

print("\nTrying to add an overlapping event at 10:30...")
try:
    schedule.add_event("Overlapping event", "2026-07-05", "10:30", 1)
except ValueError as error:
    print(error)

print("\nAdding a task...")
schedule.add_task("Finish Kaggle writeup", "2026-07-08", "high")
print(json.dumps(schedule.list_tasks(), indent=2))