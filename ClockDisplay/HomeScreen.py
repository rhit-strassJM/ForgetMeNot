import kivy
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

kivy.require("2.1.0")  # replace with your Kivy version if necessary


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Main layout for HomeScreen
        layout = BoxLayout(orientation='horizontal')

        # Add image on the right side of the screen
        image_path = 'your_image.jpg'
        if os.path.exists(image_path):
            image = Image(source=image_path)
            layout.add_widget(image)

        # Side column divided into four buttons
        button_layout = BoxLayout(orientation='vertical', size_hint=(0.25, 1))

        location_button = Button(text="Location", size_hint=(0.25, 1), on_press=self.location_press, background_color=[0.475, 0.655, 0.784], font_size=50)
        weather_button = Button(text="Weather", size_hint=(0.25, 1), on_press=self.weather_press, background_color=[0.475, 0.655, 0.784], font_size=50)
        clock_button = Button(text="Clock", size_hint=(0.25, 1), on_press=self.clock_press, background_color=[0.475, 0.655, 0.784], font_size=50)

        button_layout.add_widget(location_button)
        button_layout.add_widget(weather_button)
        button_layout.add_widget(clock_button)




        layout.add_widget(button_layout)
        self.add_widget(layout)

    def location_press(self, instance):
        App.get_running_app().show_current_location_screen()

    def weather_press(self, instance):
        App.get_running_app().show_current_weather_screen()

    def clock_press(self, instance):
        App.get_running_app().show_current_clock_screen()


if __name__ == '__main__':
    from kivy.uix.screenmanager import ScreenManager

    screen_manager = ScreenManager()
    screen_manager.add_widget(HomeScreen(name='home'))

    from kivy.base import runTouchApp
    runTouchApp(screen_manager)