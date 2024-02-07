import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle

import requests

kivy.require("2.1.0")  # replace with your Kivy version if necessary

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10)

        # Add LocationPin image
        location_pin_image = AsyncImage(source='IconImages/LocationPin.jpg', allow_stretch=False, keep_ratio=True)
        self.layout.add_widget(location_pin_image)

        self.location_label = Label(text="Fetching data...", font_size=40, color=[0, 0, 0, 1])  # Set text color to black
        self.layout.add_widget(self.location_label)

        # Set background color for the entire screen
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Background color (white)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

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

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class LocationApp(App):
    def build(self):
        screen_manager = ScreenManager()
        loading_screen = LoadingScreen(name='loading')
        screen_manager.add_widget(loading_screen)
        return screen_manager

if __name__ == "__main__":
    LocationApp().run()
