from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.app import App

class SettingsScreen(Screen):
    def create_settings_layout(self):
        # Set the background color of the window to white
        Window.clearcolor = get_color_from_hex("#FFFFFF")

        # Create a RelativeLayout as the root layout
        main_layout = RelativeLayout()

        # Create the top label with black text
        top_label = Label(
            text="Settings",
            size_hint=(1, 0.2),
            font_name="DejaVuSans",
            font_size=30,
            color=get_color_from_hex("#000000"),
            pos_hint={'top': 1}  # Position the label at the top of the screen
        )

        # Create TextInput for location
        location_input = TextInput(
            text="Terre Haute, IN",  # Set default text
            size_hint=(0.8, None),
            height=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            multiline=False,
            hint_text="Edit location...  (City, State)"
        )

        # Create Button for "Account Info"
        account_info_button = Button(
            text="Account Info",
            size_hint=(0.8, None),
            height=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_press=self.on_account_info_press
        )

        # Bind the on_text_validate event to handle location selection
        location_input.bind(on_text_validate=self.on_location_select)

        # Add the label, location input, and account info button to the layout
        main_layout.add_widget(top_label)
        main_layout.add_widget(location_input)
        main_layout.add_widget(account_info_button)

        return main_layout

    def on_location_select(self, instance):
        selected_location = instance.text
        print(f"Selected location: {selected_location}")

    def on_account_info_press(self, instance):
        print("Account Info button pressed")

    def on_enter(self, *args):
        """ Called when this screen is displayed """
        self.add_widget(self.create_settings_layout())

class SettingsApp(App):
    def build(self):
        screen_manager = ScreenManager()
        settings_screen = SettingsScreen(name='settings')
        screen_manager.add_widget(settings_screen)
        return screen_manager

if __name__ == "__main__":
    SettingsApp().run()

