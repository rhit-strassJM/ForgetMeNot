import os
from shutil import copyfile
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
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
            if self.source == 'ButtonImages/AddImage.png':
                # Show the file chooser popup
                file_chooser_popup.open()
            return True
        return super().on_touch_down(touch)

class CurrentDisplayScreen(Screen):
    def create_display_layout(self):
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
            size=(50, 50),
            pos_hint={'center_x': 0.3, 'center_y': 0.2},
            keep_ratio=False,
            allow_stretch=True,
        )

        # Create image button for "Add Alarm/Reminder"
        add_alarm_button = ImageButton(
            source='ButtonImages/AddImage.png',
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'center_x': 0.7, 'center_y': 0.2},
            keep_ratio=False,
            allow_stretch=True,
        )

        # Add buttons to the main layout
        main_layout.add_widget(add_photos_button)
        main_layout.add_widget(add_alarm_button)

        return main_layout

    def on_enter(self, *args):
        """ Called when this screen is displayed """
        self.add_widget(self.create_display_layout())

# File chooser popup content
file_chooser_content = FileChooserIconView(
    filters=['*.png', '*.jpg', '*.jpeg']
)

# Create the file chooser popup
file_chooser_popup = Popup(
    title="Choose an Image File",
    content=file_chooser_content,
    size_hint=(None, None),
    size=(400, 400),
)

class ImageFilePopup(Popup):
    def __init__(self, **kwargs):
        super(ImageFilePopup, self).__init__(**kwargs)

    def on_submit(self, instance):
        selection = file_chooser_content.selection
        if selection:
            selected_file = selection[0]
            print(f"Selected file: {selected_file}")

            # Set the destination folder
            destination_folder = os.path.join(os.path.dirname(__file__), 'DisplayImages')
            os.makedirs(destination_folder, exist_ok=True)

            # Extract the file name from the path
            file_name = os.path.basename(selected_file)

            # Set the destination path
            destination_path = os.path.join(destination_folder, file_name)

            try:
                # Copy the selected file to the destination folder
                copyfile(selected_file, destination_path)
                print(f"File saved to: {destination_path}")

                # Close the file chooser popup
                file_chooser_popup.dismiss()

                # Show the success popup
                success_popup.open()
            except Exception as e:
                print(f"Error saving file: {e}")

# Create an instance of the ImageFilePopup
image_file_popup = ImageFilePopup(title="Image File Saved", size_hint=(None, None), size=(300, 200))

# Success popup
success_popup = Popup(
    title="Success",
    content=Label(text="Image File Saved Successfully!"),
    size_hint=(None, None),
    size=(200, 150),
)

# Bind the on_submit event to the on_submit method
file_chooser_content.bind(on_submit=lambda instance, selection, touch: image_file_popup.on_submit(instance))

if __name__ == "__main__":
    CurrentDisplayApp().run()
