from schedule import add_event, add_task, read_calendar, list_tasks, find_free_slots
from google.adk.tools import FunctionTool
from google.adk.agents import Agent
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

add_event_tool = FunctionTool(add_event)
add_task_tool = FunctionTool(add_task)
read_calendar_tool = FunctionTool(read_calendar)
list_tasks_tool = FunctionTool(list_tasks)
find_free_slots_tool = FunctionTool(find_free_slots)