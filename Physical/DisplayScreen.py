import os
from shutil import copyfile

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import get_color_from_hex

from GUI.Photos import ImageFlipperApp

class CurrentDisplayScreen(Screen):
    def create_display_layout(self):
        main_layout = RelativeLayout()
        top_label = Label(
            text="TEST",
            size_hint=(1, 0.2),
            font_name="DejaVuSans",
            font_size=30,
            color=get_color_from_hex("#000000"),
            pos_hint={'top': 1}  # Position the label at the top of the screen
        )

        main_layout.add_widget(top_label)

        image_flipper_app = ImageFlipperApp()
        image_flipper_root = image_flipper_app.build()

        image_flipper_root.pos_hint = {'center_x': 0.5, 'center_y': 0.6}  # Adjust as needed
        image_flipper_root.size_hint = (0.6, 0.4)  # Adjust as needed

        main_layout.add_widget(image_flipper_root)


        return main_layout

    def on_enter(self, *args):
        """ Called when this screen is displayed """
        self.add_widget(self.create_display_layout())


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CurrentDisplayScreen(name='current_display_screen'))
        return sm


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

            destination_folder = os.path.join(os.path.dirname(__file__), 'DisplayImages')
            os.makedirs(destination_folder, exist_ok=True)

            file_name = os.path.basename(selected_file)

            destination_path = os.path.join(destination_folder, file_name)

            try:
                copyfile(selected_file, destination_path)
                print(f"File saved to: {destination_path}")

                file_chooser_popup.dismiss()

                success_popup.open()
            except Exception as e:
                print(f"Error saving file: {e}")


image_file_popup = ImageFilePopup(title="Image File Saved", size_hint=(None, None), size=(300, 200))

success_popup = Popup(
    title="Success",
    content=Label(text="Image File Saved Successfully!"),
    size_hint=(None, None),
    size=(200, 150),
)

file_chooser_content.bind(on_submit=lambda instance, selection, touch: image_file_popup.on_submit(instance))

if __name__ == '__main__':
    MyApp().run()


