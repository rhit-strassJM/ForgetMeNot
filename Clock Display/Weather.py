import json
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.network.urlrequest import UrlRequest

# API key and location
api_key = "dd9c0c4067f474a07f44c50dc890be52"
location = "Terre Haute, IN"

# Build main layout
class WeatherApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=10)

        # Label for city and country
        self.city_label = Label(text=f"Weather in {location}", font_size=20)
        layout.add_widget(self.city_label)

        # Image for weather icon
        self.weather_image = Image(source="")
        layout.add_widget(self.weather_image)

        # Label for current temperature
        self.temp_label = Label(text="", font_size=16)
        layout.add_widget(self.temp_label)

        # Load weather data and update UI
        self.get_weather()

        return layout

    # Fetch weather data using API
    def get_weather(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        request = UrlRequest(url, self.handle_weather_data)

    # Parse weather data and update UI
    def handle_weather_data(self, request):
        if request.status_code == 200:
            data = json.loads(request.content)
            weather = data["weather"][0]
            icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
            self.weather_image.source = icon_url
            self.temp_label.text = f"{int(data['main']['temp'] - 273.15)}°C"
        else:
            self.weather_image.source = "error.png"
            self.temp_label.text = "Error fetching weather data!"

    def update_weather(self, dt):
        self.get_weather()


# Run the app
if __name__ == "__main__":
    WeatherApp().run()