from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.pickers import MDTimePicker

from GUI.CurrentDisplayScreen import CurrentDisplayScreen
from GUI.LoginScreen import LoginScreen
from GUI.ReminderScreen import ReminderScreen


class TestApp(App):

    def build(self):
        sm = ScreenManager()
        # instantiate the screens
        login_screen = LoginScreen(name='login')
        reminder_screen = ReminderScreen(name='reminder')
        current_screen = CurrentDisplayScreen(name='display')

        # add to the screen manager
        sm.add_widget(login_screen)
        sm.add_widget(reminder_screen)
        sm.add_widget(current_screen)
        return sm


if __name__ == '__main__':
    TestApp().run()
