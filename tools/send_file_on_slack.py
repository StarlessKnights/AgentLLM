from parent_classes.tool import Tool

class SendFileOverSlack(Tool):
    name = "send_file_over_slack"
    description = "sends a file to a user over Slack"
    parameters = {
        "file_path": "path to file to send",
        "user_id": "the id of the user to send it to",
        "message": "the message to send along with the file"
    }
    
    @staticmethod
    def run(file_path: str, user_id: str, message: str):
        import os
        import requests
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError

        client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

        try:
            result = client.files_getUploadURLExternal(
                length=os.path.getsize(file_path),
                filename=os.path.basename(file_path),
            )

            if not result["ok"]:
                return {"status": "error", "message": result["error"]}

            file_id = result["file_id"]
            upload_url = result["upload_url"]

            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                inter_response = requests.post(
                    upload_url,
                    headers={
                        "Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"
                    },
                    files=files,
                    data={"filename": os.path.basename(file_path)}
                )

            if inter_response.status_code != 200:
                return {"status": "error", "message": "Failed to upload file to Slack"}

            try:
                dm_response = client.conversations_open(users=user_id)
                channel_id = dm_response["channel"]["id"]

                client.files_completeUploadExternal(
                    files=[{"id": file_id}],
                    channel_id=channel_id,
                    initial_comment=message,
                )
                return {"status": "success", "message": "File sent successfully"}
            except SlackApiError as e:
                return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": str(e)}