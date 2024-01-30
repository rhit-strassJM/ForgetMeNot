from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10)

        self.username_input = TextInput(multiline=False)
        self.password_input = TextInput(password=True, multiline=False)
        login_button = Button(text='Login', on_press=self.check_credentials)

        layout.add_widget(Label(text='Please Enter Username:'))
        layout.add_widget(self.username_input)
        layout.add_widget(Label(text='Please Enter Password:'))
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def check_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == 'username' and password == 'password':
            self.manager.current = 'display'
