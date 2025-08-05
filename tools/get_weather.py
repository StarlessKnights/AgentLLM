import os
from parent_classes.tool import Tool
import requests

class GetWeather(Tool):
    name = "get_weather"
    description = "Gets the current weather for a given location"
    parameters = {
        "location": "the location to get the weather for",
    }

    @staticmethod
    def run(location):
        response = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_API_KEY')}&q={location}"
        )

        if response.status_code != 200:
            return {"status": "error", "message": "Failed to get weather data"}

        data = response.json()

        return {
            "status": "success",
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
        }