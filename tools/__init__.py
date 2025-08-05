from tools.get_weather import GetWeather
from tools.get_slack_user_ids import GetSlackUserIds
from tools.send_message_on_slack import SendSlackMessage
from tools.graph_equation import GraphEquation
from tools.get_news import GetNews
from tools.send_file_on_slack import SendFileOverSlack
from tools.get_users_signed_into_thx import GetUsersSignedIntoTHX
from tools.create_csv_from_data import CreateCSVFromData
# from tools.schedule_event import ScheduleEvent
# from tools.reschedule_event import EditEvent
# from tools.delete_event import DeleteEvent
# from tools.get_event_details import GetEventDetails
from tools.run_shell_command import RunShellCommand
# from tools.get_calendar_events import GetCalendarEvents

TOOLS = [
    GetWeather,
    GetSlackUserIds,
    SendSlackMessage,
    GraphEquation,
    GetNews,
    SendFileOverSlack,
    GetUsersSignedIntoTHX,
    CreateCSVFromData,
    # ScheduleEvent,
    # EditEvent,
    # DeleteEvent,
    # GetEventDetails,
    RunShellCommand,
    # GetCalendarEvents
]

print(f"Loaded {len(TOOLS)} tools.")