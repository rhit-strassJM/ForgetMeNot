from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen

from GUI.WeatherAPI import WeatherAPI

class WeatherScreen(Screen):
    def on_enter(self, *args):
        api_key = "8f47fc536ae04a97901192639241701"
        weather_api = WeatherAPI(api_key)
        city = "Terre Haute"  # Replace with a valid city name
        weather_data = weather_api.get_weather_data(city)

        layout = BoxLayout(orientation='vertical')

        # Add labels with background color and bold text
        temperature_label = self.create_label(f"Temperature: {weather_data['temperature']}°C")
        humidity_label = self.create_label(f"Humidity: {weather_data['humidity']}%")
        condition_label = self.create_label(f"Condition: {weather_data['condition']}")
        wind_label = self.create_label(f"Wind Speed: {weather_data['wind_speed']} km/h")

        # Add labels to the layout
        layout.add_widget(temperature_label)
        layout.add_widget(humidity_label)
        layout.add_widget(condition_label)
        layout.add_widget(wind_label)

        self.add_widget(layout)

    def create_label(self, text):
        label = Label(text=text, bold=True)

        with label.canvas.before:
            Color(0.9, 0.8, 0.7)  # Background color
            self.rect = Rectangle(pos=label.pos, size=label.size)

        # Bind the rectangle's size and pos to the label's size and pos
        label.bind(size=self.update_rect, pos=self.update_rect)

        return label

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    from kivy.uix.screenmanager import ScreenManager

    screen_manager = ScreenManager()
    screen_manager.add_widget(WeatherScreen(name='weather'))

    from kivy.base import runTouchApp
    runTouchApp(screen_manager)
