from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from GUI.CurrentDisplayScreen import CurrentDisplayScreen
from GUI.LoginScreen import LoginScreen
from GUI.ReminderScreen import ReminderScreen

class TestApp(App):
    def build(self):
        self.sm = ScreenManager()
        # instantiate the screens
        self.login_screen = LoginScreen(name='login')
        self.reminder_screen = ReminderScreen(name='reminder')
        self.current_screen = CurrentDisplayScreen(name='display')

        # add to the screen manager
        self.sm.add_widget(self.login_screen)
        self.sm.add_widget(self.reminder_screen)
        self.sm.add_widget(self.current_screen)

        # Initially, show the login screen
        self.sm.current = 'login'

        return self.sm

    def show_current_display_screen(self):
        # Switch to the current display screen
        self.sm.current = 'display'

if __name__ == '__main__':
    TestApp().run()
