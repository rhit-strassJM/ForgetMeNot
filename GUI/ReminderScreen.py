from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from GUI.data_manager import reminder_entries, save_reminders
from kivy.uix.screenmanager import Screen


class ReminderScreen(Screen):
    def __init__(self, **kwargs):
        super(ReminderScreen, self).__init__(**kwargs)
        self.build()

    def build(self):
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.reminder_input = TextInput(hint_text='Enter Reminder', multiline=False, size_hint_y=None, height=30)
        self.note_input = TextInput(hint_text='Add a Note', multiline=False, size_hint_y=None, height=30)

        entry_box = BoxLayout(orientation='horizontal', spacing=10)
        entry_box.add_widget(self.reminder_input)
        entry_box.add_widget(self.note_input)

        self.root.add_widget(entry_box)

        self.date_button = Button(text='Select Date', on_press=self.show_date_picker, size_hint_y=None, height=30)
        self.root.add_widget(self.date_button)

        self.time_spinner = Spinner(text='Select Time', values=['12:00 AM', '01:00 AM', '02:00 AM', '03:00 AM', '04:00 AM',
                                                                '05:00 AM', '06:00 AM', '07:00 AM', '08:00 AM', '09:00 AM',
                                                                '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM',
                                                                '03:00 PM', '04:00 PM', '05:00 PM', '06:00 PM', '07:00 PM',
                                                                '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM'],
                                    size_hint_y=None, height=30)
        self.root.add_widget(self.time_spinner)

        self.audio_button = Button(text='Select Audio', on_press=self.show_audio_chooser, size_hint_y=None, height=30)
        self.root.add_widget(self.audio_button)

        add_button = Button(text='Add Reminder', on_press=self.add_reminder)
        self.root.add_widget(add_button)

        self.reminder_container = BoxLayout(orientation='vertical', spacing=10)
        self.root.add_widget(self.reminder_container)

        return self.root

    def show_date_picker(self, instance):
        date_popup = Popup(title='Select Date', size_hint=(None, None), size=(300, 300))
        date_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        day_spinner = Spinner(text='Day', values=[str(i) for i in range(1, 32)])
        month_spinner = Spinner(text='Month', values=[str(i) for i in range(1, 13)])
        year_spinner = Spinner(text='Year', values=[str(i) for i in range(2022, 2030)])

        date_layout.add_widget(day_spinner)
        date_layout.add_widget(month_spinner)
        date_layout.add_widget(year_spinner)

        set_date_button = Button(text='Set Date', on_press=lambda x: self.set_selected_date(date_popup,
                                                                                           day_spinner.text,
                                                                                           month_spinner.text,
                                                                                           year_spinner.text))

        date_layout.add_widget(set_date_button)
        date_popup.content = date_layout
        date_popup.open()

    def show_audio_chooser(self, instance):
        audio_popup = Popup(title='Select Audio File', size_hint=(None, None), size=(400, 400))
        audio_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        file_chooser = FileChooserListView()
        audio_layout.add_widget(file_chooser)

        set_audio_button = Button(text='Set Audio', on_press=lambda x: self.set_selected_audio(audio_popup, file_chooser.path))

        audio_layout.add_widget(set_audio_button)
        audio_popup.content = audio_layout
        audio_popup.open()

    def set_selected_date(self, date_popup, day, month, year):
        selected_date = f'{month}/{day}/{year}'
        self.date_button.text = selected_date
        date_popup.dismiss()

    def set_selected_audio(self, audio_popup, selected_path):
        audio_popup.dismiss()

    def add_reminder(self, instance):
        reminder_text = self.reminder_input.text
        note_text = self.note_input.text
        time_text = self.time_spinner.text
        date_text = self.date_button.text

        if reminder_text:
            reminder_entry = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=100)

            reminder_label = Label(text=f'Reminder: {reminder_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(reminder_label)

            note_label = Label(text=f'Note: {note_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(note_label)

            time_label = Label(text=f'Time: {time_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(time_label)

            date_label = Label(text=f'Date: {date_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(date_label)

            self.reminder_container.add_widget(reminder_entry)

            reminder_entries.append({
                'text': reminder_text,
                'note': note_text,
                'time': time_text,
                'date': date_text,
                'audio_path': None
            })

            self.reminder_input.text = ''
            self.note_input.text = ''
            self.time_spinner.text = 'Select Time'
            self.date_button.text = ''

            save_reminders(reminder_entries)


