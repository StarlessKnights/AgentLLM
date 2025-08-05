from parent_classes.tool import Tool
from services.firebase import get_people_signed_in

class GetUsersSignedIntoTHX(Tool):
    name = "get_users_signed_into_thx"
    description = "gets the users signed into torque hours x"
    parameters = {}

    @staticmethod
    def run():
        try:
            people_signed_in = get_people_signed_in()
        except Exception as e:
            return {"status": "error", "message": f"Failed to get people signed in: {e}"}
        return {"status": "success", "data": people_signed_in}