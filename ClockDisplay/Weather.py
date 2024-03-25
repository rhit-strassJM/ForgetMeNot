from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle

from ClockDisplay.WeatherAPI import WeatherAPI

class WeatherScreen(Screen):
    def on_enter(self, *args):
        api_key = "8f47fc536ae04a97901192639241701"
        weather_api = WeatherAPI(api_key)
        city = "Terre Haute"  # Replace with a valid city name
        weather_data = weather_api.get_weather_data(city)

        layout = BoxLayout(orientation='horizontal', spacing=10, padding=10)

        # Determine which image to use based on the weather condition
        if weather_data['condition'].lower() == "sunny":
            image_source = 'IconImages/Rainy.jpg'
        elif weather_data['condition'].lower() == "partly cloudy":
            image_source = 'IconImages/Rainy.jpg'
        elif weather_data['condition'].lower() == "partly rainy":
            image_source = 'IconImages/Rainy.jpg'
        else:
            # Use a default image for other conditions
            image_source = 'IconImages/Sunny.jpg'

        left_image = AsyncImage(source=image_source, allow_stretch=False, keep_ratio=True)
        layout.add_widget(left_image)

        # Create a vertical BoxLayout for labels and right image
        label_layout = BoxLayout(orientation='vertical', spacing=10)

        # Add labels with bold text and larger font size
        temperature_label = self.create_label(f"Temperature: {weather_data['temperature']}°C", font_size=70)
        humidity_label = self.create_label(f"Humidity: {weather_data['humidity']}%", font_size=70)
        condition_label = self.create_label(f"Condition: {weather_data['condition']}", font_size=70)
        wind_label = self.create_label(f"Wind Speed: {weather_data['wind_speed']} km/h", font_size=70)

        # Add labels to the vertical layout
        label_layout.add_widget(temperature_label)
        label_layout.add_widget(humidity_label)
        label_layout.add_widget(condition_label)
        label_layout.add_widget(wind_label)

        # Add the label layout to the main layout
        layout.add_widget(label_layout)

        # Set background color for the entire screen
        with self.canvas.before:
            Color(0.529, 0.808, 0.922, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.add_widget(layout)

    def create_label(self, text, font_size):
        label = Label(text=text, bold=True, color=[0, 0, 0, 1], font_size=font_size)  # Black text
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
