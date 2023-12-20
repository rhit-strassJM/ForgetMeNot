from kivy.app import App
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.config import Config

# Set window size
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

# Importing ImageFlipperApp from the other file
from Photos import ImageFlipperApp

class ImageButton(Image):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(f"{self.source} button pressed")
            return True
        return super().on_touch_down(touch)

class CurrentDisplayApp(App):
    def build(self):
        # Set the background color of the window to white
        Window.clearcolor = get_color_from_hex("#FFFFFF")

        # Create a RelativeLayout as the root layout
        main_layout = RelativeLayout()

        # Create the top label with black text
        top_label = Label(
            text="Current Display",
            size_hint=(1, 0.2),
            font_name="DejaVuSans",
            font_size=30,
            color=get_color_from_hex("#000000"),
            pos_hint={'top': 1}  # Position the label at the top of the screen
        )

        # Add the label to the layout
        main_layout.add_widget(top_label)

        # Create an instance of ImageFlipperApp
        image_flipper_app = ImageFlipperApp()

        # Build the ImageFlipperApp and get its root widget
        image_flipper_root = image_flipper_app.build()

        # Set the position and size of the ImageFlipper root widget
        image_flipper_root.pos_hint = {'center_x': 0.5, 'center_y': 0.6}  # Adjust as needed
        image_flipper_root.size_hint = (0.6, 0.4)  # Adjust as needed

        # Add the ImageFlipper root widget to the main layout
        main_layout.add_widget(image_flipper_root)

        # Create image button for "Add Photos"
        add_photos_button = ImageButton(
            source='ButtonImages/AddAlarm.png',
            size_hint=(None, None),
            size=(150, 100),
            pos_hint={'center_x': 0.3, 'center_y': 0.2},
        )

        # Create image button for "Add Alarm/Reminder"
        add_alarm_button = ImageButton(
            source='ButtonImages/AddImage.png',
            size_hint=(None, None),
            size=(150, 100),
            pos_hint={'center_x': 0.7, 'center_y': 0.2},
        )

        # Add buttons to the main layout
        main_layout.add_widget(add_photos_button)
        main_layout.add_widget(add_alarm_button)

        return main_layout

if __name__ == "__main__":
    CurrentDisplayApp().run()