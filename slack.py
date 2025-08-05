import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from main import run_it

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

class Slack():
    def __init__(self) -> None:
        pass

    @app.message("llm")
    def message_hello(message, say):
        say("pls give me a second to think 🤔...")
        try:
            res = run_it(message["text"]) # type: ignore

            say(
                text=f"{res}"
            )
        except:
            say("something went wrong whoops.")

    def run(self) -> None:
        SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()

slack = Slack()
slack.run()
