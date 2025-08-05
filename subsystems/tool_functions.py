from dotenv import load_dotenv
from tool_memory import ToolMemory
from subsystems.memory import Memory
from collections.abc import Callable
from tools import *

load_dotenv()
memory = ToolMemory()

def search_tools(query: str):
    results = memory.search(query)
    tools = [
        {"tool": tool["name"], "args": tool["args"]}
        for tool in results.get('tools', [])
    ]

    return tools

def run_tool(tool_id: str, kwargs: dict):
    if tool_id in tool_mapping:
        result = tool_mapping[tool_id](**kwargs)
        return result
    else:
        return {"status": "error", "message": f"Tool {tool_id} not found."}
    
def append_to_memory(text: str):
    doc_mem = Memory()
    doc_mem.add(text)
    return {"status": "success", "message": "Text appended to memory."}

tool_mapping: dict[str, Callable] = {
    "get_weather": GetWeather.run,
    "get_slack_user_ids": GetSlackUserIds.run,
    "send_slack_message": SendSlackMessage.run,
    "graph_equation": GraphEquation.run,
    "send_file_over_slack": SendFileOverSlack.run,
    "get_news": GetNews.run,
    "get_users_signed_into_thx": GetUsersSignedIntoTHX.run,
    "create_csv_from_data": CreateCSVFromData.run,
    # "schedule_event": ScheduleEvent.run,
    # "edit_event": EditEvent.run,
    # "delete_event": DeleteEvent.run,
    # "get_event_details": GetEventDetails.run,
    "run_shell_command": RunShellCommand.run,
    # "get_calendar_events": GetCalendarEvents.run,
}