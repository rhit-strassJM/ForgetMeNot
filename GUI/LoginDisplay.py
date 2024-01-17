from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from GUI.CurrentDisplay import CurrentDisplayScreen


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

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Welcome to the second screen!'))

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CurrentDisplayScreen(name='display'))
        return sm

if __name__ == '__main__':
    MyApp().run()
