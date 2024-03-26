from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ClockDisplay.Location import LocationScreen
from ClockDisplay.Weather import WeatherScreen
from ClockDisplay.HomeScreen import HomeScreen
from ClockDisplay.Clock import ClockScreen
from kivymd.app import MDApp

class DisplayApp(MDApp):

    def build(self):
        self.sm = ScreenManager()
        self.home_screen = HomeScreen(name='home')
        self.clock_screen = ClockScreen(name='clock')
        self.weather_screen = WeatherScreen(name='weather')
        self.location_screen = LocationScreen(name='location')


        self.sm.add_widget(self.home_screen)
        self.sm.add_widget(self.clock_screen)
        self.sm.add_widget(self.weather_screen)
        self.sm.add_widget(self.location_screen)


        self.sm.current = 'home'

        return self.sm

    def show_current_clock_screen(self):
        self.sm.current = 'clock'

    def show_current_weather_screen(self):
        self.sm.current = 'weather'

    def show_current_location_screen(self):
        self.sm.current = 'location'


if __name__ == '__main__':
    DisplayApp().run()
