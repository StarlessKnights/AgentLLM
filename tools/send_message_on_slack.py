from parent_classes.tool import Tool
import requests
import os

class SendSlackMessage(Tool):
    name = "send_slack_message"
    description = "sends a message to a user"
    parameters = {
        "user_id": "user to send message to (require get_slack_user_ids)",
        "message": "message to send to the user (cannot embed files with this tool)",
    }
    
    @staticmethod
    def run(user_id, message):
        print(f"\033[91mllm is requesting to send this message: {message}\033[0m")
        confirmation = ""

        while confirmation not in ["yes", "no"]:
            confirmation = input("Do you want to send this message? (yes/no): ")

        match confirmation:
            case "yes":
                headers = {
                    "Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"
                    }
                data = {
                    "channel": user_id,
                    "text": message
                }
                response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=data).json()

                if response["ok"]:
                    return {"status": "success"}
                else:
                    return {"status": "denied", "data": f"Error: {response['error']}"}
            case "no":
                return {"status": "denied", "data": "Your request to send the message was denied."}     