from parent_classes.tool import Tool
import requests
import os

class GetSlackUserIds(Tool):
    name = "get_slack_user_ids"
    description = "gets the user IDs of users in the slack channel"
    parameters = {}

    @staticmethod
    def run():
        headers = {
            "Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"
        }

        allowed_user_names = ["Tima Gezalov", "Davis Jenney", "Julianna Griepp", "Ryan Nirmal", "Farzaan Z", "Claudia Zinngrabe", "Davey Adams", "Maaz Kattangere", "Owen Ye", "Uma Warrier", "Aaron Raj", "Luke Liu", "Sahil Kulkarni", "D.A.V.E"]

        response = requests.get("https://slack.com/api/users.list", headers=headers).json()

        if response["ok"]:
            user_name_to_id_mapping = {user["profile"]["real_name"]: user["id"] for user in response["members"] if user["profile"]["real_name"] in allowed_user_names}
            return {"status": "success", "data": user_name_to_id_mapping}
        else:
            return {"status": "error", "message": response["error"]}