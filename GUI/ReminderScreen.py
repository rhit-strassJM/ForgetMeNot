from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

class ReminderScreen(Screen):
    name = 'reminder'
    def __init__(self, **kwargs):
        super(ReminderScreen, self).__init__(**kwargs)

        # Create layout
        self.layout = BoxLayout(orientation='vertical')

        # Add title label
        self.title_label = Label(text='Reminder', font_size=30)
        self.layout.add_widget(self.title_label)

        # Add date and time input fields
        self.date_input = TextInput(hint_text='Select Date')
        self.time_input = TextInput(hint_text='Select Time')
        self.layout.add_widget(self.date_input)
        self.layout.add_widget(self.time_input)

        # Add note input field
        self.note_input = TextInput(hint_text='Enter Note')
        self.layout.add_widget(self.note_input)

        # Add buttons for date, time, and save
        self.date_button = Button(text='Select Date')
        self.date_button.bind(on_press=self.show_date_picker)
        self.time_button = Button(text='Select Time')
        self.time_button.bind(on_press=self.show_time_picker)
        self.add_audio_button = Button(text='Add Audio')
        self.add_audio_button.bind(on_press=self.show_audio_popup)
        self.save_button = Button(text='Save Reminder')
        self.save_button.bind(on_press=self.save_reminder)
        self.layout.add_widget(self.date_button)
        self.layout.add_widget(self.time_button)
        self.layout.add_widget(self.add_audio_button)
        self.layout.add_widget(self.save_button)

        # Add layout to screen
        self.add_widget(self.layout)

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def show_time_picker(self, instance):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save)
        time_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.date_input.text = value.strftime('%Y-%m-%d')

    def on_time_save(self, instance, value):
        self.time_input.text = value.strftime('%H:%M')

    def show_audio_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path='.', filters=['*.wav'])
        content.add_widget(file_chooser)
        popup = Popup(title='Select Audio File', content=content, size_hint=(0.9, 0.9))
        select_button = Button(text='Select')
        select_button.bind(on_press=lambda btn: self.on_audio_selected(popup, file_chooser))
        content.add_widget(select_button)
        popup.open()

    def on_audio_selected(self, popup, file_chooser):
        selected_file = file_chooser.selection and file_chooser.selection[0] or None
        if selected_file:
            self.audio_file_path = selected_file
            popup.dismiss()

    def save_reminder(self, instance):
        date = self.date_input.text
        time = self.time_input.text
        note = self.note_input.text

        # Here you can save the reminder with the provided information
        print(f"Reminder saved: Date - {date}, Time - {time}, Note - {note}, Audio File - {self.audio_file_path}")

# Example usage:
# You need to handle the audio file selection and saving logic accordingly
# The code above prints the selected audio file path for demonstration purposes
