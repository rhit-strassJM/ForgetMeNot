import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
import requests

kivy.require("2.1.0")  # replace with your Kivy version if necessary

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10)
        self.location_label = Label(text="Fetching data...")
        self.layout.add_widget(self.location_label)
        self.add_widget(self.layout)

    def on_enter(self):
        try:
            location_info = self.get_location_info()
            self.update_location(location_info)
        except Exception as e:
            print(f"Error fetching location: {e}")
            self.location_label.text = "Error fetching location data."

    def get_location_info(self):
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        return response.json()

    def update_location(self, location_info):
        if "city" in location_info:
            city = location_info["city"]
            self.location_label.text = f"Current Location: {city}"

            if "loc" in location_info:
                latitude, longitude = location_info["loc"].split(",")
                self.location_label.text += f"\nLatitude: {latitude}, Longitude: {longitude}"
        else:
            self.location_label.text = "Location information not available."

class LocationApp(App):
    def build(self):
        screen_manager = ScreenManager()
        loading_screen = LoadingScreen(name='loading')
        screen_manager.add_widget(loading_screen)
        return screen_manager

if __name__ == "__main__":
    LocationApp().run()
