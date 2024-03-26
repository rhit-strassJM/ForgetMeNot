# ClockDisplay/another_file.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import RoundedRectangle, Color
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window  # Import Window to set background color

from GUI.data_manager import reminder_entries
from kivy.uix.screenmanager import Screen



class RoundedBackground(BoxLayout):
    radius = NumericProperty(10)
    color = [0.9, 0.8, 0.7]

    def __init__(self, text='', note='', time='', **kwargs):
        super(RoundedBackground, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.size_hint_y = None
        self.height = 100
        self.padding = 10
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.reminder_label = Label(text=f'Reminder: {text}', color=(0, 0, 0, 1))
        self.note_label = Label(text=f'Note: {note}', color=(0, 0, 0, 1))
        self.time_label = Label(text=f'Time: {time}', color=(0, 0, 0, 1))

        self.add_widget(self.reminder_label)
        self.add_widget(self.note_label)
        self.add_widget(self.time_label)

    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius, self.radius, self.radius, self.radius])


class ReminderDisplay(Screen):
    def build(self):
        # Set the background color of the Window
        Window.clearcolor = (1, 1, 1, 1)

        root = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll_view = ScrollView()

        reminders_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        reminders_container.bind(minimum_height=reminders_container.setter('height'))

        for entry in reminder_entries:
            reminder_entry = RoundedBackground(text=entry['text'], note=entry['note'], time=entry['time'])
            reminders_container.add_widget(reminder_entry)

        scroll_view.add_widget(reminders_container)
        root.add_widget(scroll_view)

        return root


if __name__ == '__main__':
    from kivy.uix.screenmanager import ScreenManager

    screen_manager = ScreenManager()
    screen_manager.add_widget(ReminderDisplay(name='reminders'))

    from kivy.base import runTouchApp

    runTouchApp(screen_manager)