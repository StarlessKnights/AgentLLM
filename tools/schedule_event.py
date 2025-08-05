from parent_classes.tool import Tool
from services.google_integration import schedule_event

class ScheduleEvent(Tool):
    name = "schedule_event"
    description = "Schedules an event on the user's Google Calendar. Requires date and time."
    parameters = {
        "date": "YYYY-MM-DD",
        "time": "HH:MM (24h)",
        "end_time": "HH:MM (24h)",
        "description": "Event description (optional)",
        "summary": "Event summary (optional, defaults to 'Scheduled Event')",
    }

    @staticmethod
    def run(date, time, end_time, description="", summary=""):
        result = schedule_event(date, time, end_time, description, summary)
        return result
