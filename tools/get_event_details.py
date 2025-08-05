from parent_classes.tool import Tool
from services.google_integration import get_event_details

class GetEventDetails(Tool):
    name = "get_event_details"
    description = "Gets details of a Google Calendar event. Requires event_id."
    parameters = {
        "event_id": "Event ID"
    }

    @staticmethod
    def run(event_id):
        return get_event_details(event_id)
