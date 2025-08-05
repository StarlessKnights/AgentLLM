from parent_classes.tool import Tool
from services.google_integration import reschedule_event

class EditEvent(Tool):
    name = "edit_event"
    description = "Edits an existing Google Calendar event. Requires event_id, new_date, and new_time."
    parameters = {
        "event_id": "Event ID (required)",
        "new_date": "YYYY-MM-DD (required)",
        "new_time": "HH:MM (24h) (required)",
        "new_end_time": "HH:MM (24h) (required)",
        "new_summary": "Summary (optional)",
        "new_description": "Description (optional)",
    }

    @staticmethod
    def run(event_id, new_date, new_time, new_end_time, new_summary="", new_description=""):
        return reschedule_event(event_id, new_date, new_time, new_end_time, new_summary, new_description)