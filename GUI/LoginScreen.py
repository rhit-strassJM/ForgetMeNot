from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

Builder.load_string('''
<LoginScreen>:
    canvas.before:
        Color:
            rgb: 0.820, 0.925, 1
        Rectangle:
            pos: self.pos
            size: self.size
''')


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=50, spacing=50)

        self.username_input = TextInput(hint_text='Enter Username', multiline=False, size_hint_y=None, height=50)
        self.password_input = TextInput(hint_text='Enter Password', password=True, multiline=False, size_hint_y=None, height=50)
       # rgb(121, 167, 200)
        login_button = Button(text='Login', on_press=self.check_credentials, background_color=[0.475, 0.655, 0.784])

        image = AsyncImage(source='DisplayImages/Logo.png', size_hint_y=None, height=350)
        layout.add_widget(image)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)



        self.add_widget(layout)

    def check_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == 'username' and password == 'password':
            App.get_running_app().show_current_display_screen()
