from parent_classes.tool import Tool
from services.google_integration import delete_event

class DeleteEvent(Tool):
    name = "delete_event"
    description = "Deletes a Google Calendar event. Requires event_id."
    parameters = {
        "event_id": "Event ID"
    }

    @staticmethod
    def run(event_id):
        return delete_event(event_id)
