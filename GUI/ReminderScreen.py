from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.clock import Clock


class ReminderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_spinner = Spinner(
            text='Select Time',
            values=('00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'),
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.time_spinner.bind(text=self.set_alarm)
        self.add_widget(self.time_spinner)

        self.alarm_time = None
        self.alarm_id = None

    def set_alarm(self, instance, time):
        self.alarm_time = time

    def start_alarm(self):
        if self.alarm_id is not None:
            Clock.unschedule(self.alarm_id)
        self.alarm_id = Clock.schedule_interval(self.fire_alarm, 1)

    def fire_alarm(self, dt):
        if self.alarm_time is not None and self.alarm_time == self.time_picker.time:
            print("Alarm!")
            self.stop_alarm()
        return False

    def stop_alarm(self):
        if self.alarm_id is not None:
            Clock.unschedule(self.alarm_id)
            self.alarm_id = None
