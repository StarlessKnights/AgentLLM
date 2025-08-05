from parent_classes.tool import Tool
from services.google_integration import get_calendar_events

class GetCalendarEvents(Tool):
    name = "get_calendar_events"
    description = "gets the upcoming calendar events given a date.."
    parameters = {
        "date": "YYYY-MM-DD",
    }
    
    @staticmethod
    def run(date):
        events = get_calendar_events(date)
        if isinstance(events, str):
            return {"status": "error", "message": events}
        
        return {
            "status": "success",
            "events": events
        }