import os
from shutil import copyfile
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex

from GUI.ImageButton import ImageButton
from Photos import ImageFlipperApp
from Physical.DisplayScreen import success_popup


class CurrentDisplayScreen(Screen):
    def __init__(self, **kwargs):
        super(CurrentDisplayScreen, self).__init__(**kwargs)

        # Create the file chooser popup
        self.file_chooser_content = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        self.file_chooser_popup = Popup(title="Choose an Image File",
                                        content=self.file_chooser_content,
                                        size_hint=(None, None),
                                        size=(400, 400))
        self.file_chooser_content.bind(on_submit=self.image_file_popup_on_submit)

    def create_display_layout(self):
        Window.clearcolor = get_color_from_hex("#FFFFFF")
        main_layout = RelativeLayout()
        top_label = Label(
            text="Current Display",
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

        add_photos_button = ImageButton(
            self.manager,
            self.file_chooser_popup,
            source='ButtonImages/AddAlarm.png',
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'center_x': 0.3, 'center_y': 0.2},
            keep_ratio=False,
            allow_stretch=True,
        )

        add_alarm_button = ImageButton(
            self.manager,
            self.file_chooser_popup,
            source='ButtonImages/AddImage.png',
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'center_x': 0.7, 'center_y': 0.2},
            keep_ratio=False,
            allow_stretch=True,
        )

        main_layout.add_widget(add_photos_button)
        main_layout.add_widget(add_alarm_button)

        return main_layout

    def on_enter(self, *args):
        """ Called when this screen is displayed """
        self.add_widget(self.create_display_layout())

    def image_file_popup_on_submit(self, instance, selection, touch):
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

                self.file_chooser_popup.dismiss()

                success_popup.open()
            except Exception as e:
                print(f"Error saving file: {e}")

class ImageFilePopup(Popup):
    def __init__(self, **kwargs):
        super(ImageFilePopup, self).__init__(**kwargs)

