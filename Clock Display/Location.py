import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import requests

kivy.require("2.1.0")  # replace with your Kivy version if necessary

class LocationApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=10)

        self.location_label = Label(text="Current Location: Fetching data...")
        self.layout.add_widget(self.location_label)

        try:
            location_info = self.get_location_info()
            self.update_location(location_info)
        except Exception as e:
            print(f"Error fetching location: {e}")
            self.location_label.text = "Error fetching location data."

        return self.layout

    def get_location_info(self):
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        return response.json()

    def update_location(self, location_info):
        if "loc" in location_info:
            latitude, longitude = location_info["loc"].split(",")
            self.location_label.text = f"Current Location: Latitude {latitude}, Longitude {longitude}"
        else:
            self.location_label.text = "Location information not available."

if __name__ == "__main__":
    LocationApp().run()