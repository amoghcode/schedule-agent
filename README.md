# Schedule Agent

Schedule Agent is an AI-powered personal scheduling assistant built for the Kaggle AI Agents capstone project. It uses Google ADK to connect a Gemini-powered agent to deterministic Python tools for reading a calendar, adding events, adding tasks, and finding free time.

The project focuses on a practical scheduling workflow: instead of only generating text, the agent can call real tools that inspect and update schedule data stored in `schedule.json`.

## Problem

Students and busy individuals often manage tasks, classes, meetings, and deadlines across scattered notes or apps. This project explores how an AI agent can make that process easier by letting a user ask scheduling questions in natural language while the assistant safely uses tools to check availability and update structured data.

## Solution

The assistant can:

- Add calendar events with a date, start time, and duration.
- Add tasks with a deadline and priority.
- Read the saved calendar.
- List saved tasks.
- Find free time slots for a specific date.
- Prevent overlapping events in code.
- Normalize dates to `YYYY-MM-DD` and times to `HH:MM`.
- Keep schedule data readable in a local JSON file.

## Architecture

```text
User prompt
    |
    v
Google ADK Agent in scheduler/agent.py
    |
    v
Function tools wrapping schedule.py
    |
    v
schedule.json local calendar/task storage
```

The project has two main layers:

- `scheduler/agent.py`: defines the ADK agent, model, instructions, and function tools.
- `schedule.py`: contains deterministic scheduling logic and JSON persistence.

## Key Agent Concepts Demonstrated

- **Agent / ADK system:** the project defines a Google ADK `Agent` with tool access.
- **Tool use:** scheduling functions are exposed as `FunctionTool` objects.
- **Security and safety:** API keys are loaded from `.env`, not committed to code; event conflicts are blocked in Python; the agent prompt asks for confirmation before writes.
- **Deployability / reproducibility:** setup instructions, requirements, sample data, and a local demo script are included.

## Project Structure

```text
schedule-agent/
+-- README.md
+-- requirements.txt
+-- demo.py
+-- schedule.py
+-- schedule.json
+-- scheduler/
    +-- __init__.py
    +-- agent.py
+-- docs/
    +-- ROADMAP.md
    +-- COMPETITION_WRITEUP_OUTLINE.md
```

## Tools Exposed to the Agent

| Tool | Purpose |
| --- | --- |
| `add_event` | Adds a fixed calendar event after checking for conflicts. |
| `add_task` | Adds a task with a normalized deadline and priority. |
| `read_calendar` | Returns all saved calendar events. |
| `list_tasks` | Returns all saved tasks. |
| `find_free_slots` | Finds available time windows on a specific date. |

## Setup for Evaluators

1. Clone the repository:

```bash
git clone https://github.com/amoghcode/schedule-agent.git
cd schedule-agent
```

2. Create and activate a virtual environment:

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file for running the ADK agent:

```text
GOOGLE_API_KEY=your_google_api_key_here
```

Do not commit `.env` to GitHub. It is already listed in `.gitignore`.

## Run the Local Demo

The demo script exercises the scheduling tools without requiring an API key. It uses a temporary JSON database, so it does not modify `schedule.json`.

```bash
python demo.py
```

The demo shows:

- reading calendar events,
- finding free time on a specific date,
- adding a valid event,
- blocking an overlapping event,
- adding a task.

## Run the ADK Agent

The ADK agent is defined as `root_agent` in `scheduler/agent.py`.

Depending on your local ADK setup, run the agent from the project root with the ADK development command used in your environment. For example:

```bash
adk run scheduler
```

If your ADK setup uses a web/dev UI instead:

```bash
adk web
```

Then select the `scheduler` agent.

## Example Prompts

```text
What events are on my calendar?
```

```text
Find me a 90-minute free slot on 2026-07-05 between 09:00 and 17:00.
```

```text
Add a study session on 2026-07-05 at 10:00 for one hour.
```

```text
Add my machine learning quiz due on 2026-07-10 with high priority.
```

## Sample Data Format

```json
{
  "tasks": [
    {
      "name": "Finish Kaggle writeup",
      "deadline": "2026-07-08",
      "priority": "high"
    }
  ],
  "events": [
    {
      "name": "Project meeting",
      "date": "2026-07-05",
      "time": "14:00",
      "duration": 1
    }
  ]
}
```

Dates use `YYYY-MM-DD`. Times use 24-hour `HH:MM`.

## Current Limitations

- Storage is a local JSON file rather than a production database.
- There is no Google Calendar or Telegram integration yet.
- There is no web UI yet.
- Automated tests are not included yet; `demo.py` is provided as a repeatable evaluator demo.

## Roadmap

Near-term improvements:

- Add automated tests for the scheduling functions.
- Add a cleaner command-line interface.
- Improve validation and error messages.
- Add task-to-calendar scheduling.

Future integrations:

- Google Calendar API sync.
- Telegram bot interface.
- SQLite or cloud database storage.

## Competition Notes

This version intentionally focuses on a reliable local scheduling agent before adding external integrations. Google Calendar and Telegram are strong future directions, but the current submission prioritizes clear agent architecture, deterministic tool use, safe scheduling behavior, and reproducible evaluator setup.

## License

No license has been added yet.
