from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

from ClockDisplay.WeatherAPI import WeatherAPI

class WeatherScreen(Screen):
    def on_enter(self, *args):
        api_key = "8f47fc536ae04a97901192639241701"
        weather_api = WeatherAPI(api_key)
        city = "Terre Haute"  # Replace with a valid city name
        weather_data = weather_api.get_weather_data(city)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Add labels with bold text
        temperature_label = self.create_label(f"Temperature: {weather_data['temperature']}°C")
        humidity_label = self.create_label(f"Humidity: {weather_data['humidity']}%")
        condition_label = self.create_label(f"Condition: {weather_data['condition']}")
        wind_label = self.create_label(f"Wind Speed: {weather_data['wind_speed']} km/h")

        # Add labels to the layout
        layout.add_widget(temperature_label)
        layout.add_widget(humidity_label)
        layout.add_widget(condition_label)
        layout.add_widget(wind_label)

        # Set background color for the entire screen
        with self.canvas.before:
            Color(0.529, 0.808, 0.922, 1)  # Background color (beige)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.add_widget(layout)

    def create_label(self, text):
        label = Label(text=text, bold=True, color=[0, 0, 0, 1])  # Black text
        return label

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

if __name__ == '__main__':
    from kivy.uix.screenmanager import ScreenManager

    screen_manager = ScreenManager()
    screen_manager.add_widget(WeatherScreen(name='weather'))

    from kivy.base import runTouchApp
    runTouchApp(screen_manager)
