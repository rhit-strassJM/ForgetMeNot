from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from GUI.CurrentDisplayScreen import CurrentDisplayScreen
from GUI.LoginScreen import LoginScreen
from GUI.ReminderScreen import ReminderScreen

class App(App):

    def build(self):
        self.sm = ScreenManager()
        self.login_screen = LoginScreen(name='login')
        self.reminder_screen = ReminderScreen(name='reminder')
        self.current_screen = CurrentDisplayScreen(name='display')

        self.sm.add_widget(self.login_screen)
        self.sm.add_widget(self.reminder_screen)
        self.sm.add_widget(self.current_screen)

        self.sm.current = 'login'

        return self.sm

    def show_current_display_screen(self):
        self.sm.current = 'display'

    def show_current_reminder_screen(self):
        self.sm.current = 'reminder'


if __name__ == '__main__':
    App().run()
