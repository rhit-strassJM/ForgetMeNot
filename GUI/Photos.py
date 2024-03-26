import os
import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation

kivy.require("2.1.0")  # replace with your Kivy version if necessary

class ImageFlipperScreen(Screen):
    def build(self):
        self.layout = BoxLayout(orientation="vertical")

        # Get the current directory of the script
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Directory containing images
        images_directory = os.path.join(current_directory, "DisplayImages")

        # List of image filenames
        self.image_filenames = self.get_image_files(images_directory)
        self.current_image_index = 0

        # Create the Image widget
        self.image_widget = Image(source=self.image_filenames[self.current_image_index])
        self.layout.add_widget(self.image_widget)

        # Schedule image flipping every 5 seconds
        Clock.schedule_interval(self.flip_image, 5)

        return self.layout

    def get_image_files(self, directory):
        # Get all files in the directory
        all_files = os.listdir(directory)

        # Filter out only files with .jpg extension
        image_files = [file for file in all_files if file.lower().endswith(('.jpg', '.jpeg', 'png'))]

        # Sort the image filenames based on their numeric part
        image_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

        # Add directory path to filenames
        return [os.path.join(directory, filename) for filename in image_files]

    def flip_image(self, dt):
        # Increment the image index
        self.current_image_index = (self.current_image_index + 1) % len(self.image_filenames)

        # Create fade-in and fade-out animations
        fade_out = Animation(opacity=0, duration=1)
        fade_in = Animation(opacity=1, duration=1)

        # Define callback for when fade-out animation completes
        def fade_out_complete(animation, widget):
            # Update the Image widget with the new image
            self.image_widget.source = self.image_filenames[self.current_image_index]

            # Start the fade-in animation
            fade_in.start(self.image_widget)

        # Bind the callback to the fade-out animation
        fade_out.bind(on_complete=fade_out_complete)

        # Start the fade-out animation
        fade_out.start(self.image_widget)

    def get_layout(self):
        return self.layout

if __name__ == "__main__":
    from kivy.uix.screenmanager import ScreenManager

    screen_manager = ScreenManager()
    screen_manager.add_widget(ImageFlipperScreen(name='photos'))

    from kivy.base import runTouchApp

    runTouchApp(screen_manager)