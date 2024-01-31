import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather_data(self, city):
        api_url = f"https://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city}"

        response = requests.get(api_url)
        data = response.json()

        if "error" in data:
            print(f"Error: {data['error']['message']}")
            return {"temperature": "N/A", "humidity": "N/A", "condition": "N/A", "wind_speed": "N/A"}

        condition_data = data["current"].get("condition", {})

        return {
            "temperature": data["current"].get("temp_c", "N/A"),
            "humidity": data["current"].get("humidity", "N/A"),
            "condition": condition_data.get("text", "N/A"),
            "wind_speed": data["current"].get("wind_kph", "N/A"),
            # Add more data fields as needed
        }

