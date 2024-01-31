import os
import wave

import pyaudio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from GUI.data_manager import reminder_entries, save_reminders


class ReminderApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Entry Boxes for Reminder, Note
        self.reminder_input = TextInput(hint_text='Enter Reminder', multiline=False, size_hint_y=None, height=30)
        self.note_input = TextInput(hint_text='Add a Note', multiline=False, size_hint_y=None, height=30)

        entry_box = BoxLayout(orientation='horizontal', spacing=10)
        entry_box.add_widget(self.reminder_input)
        entry_box.add_widget(self.note_input)

        self.root.add_widget(entry_box)

        # Button for selecting date
        self.date_button = Button(text='Select Date', on_press=self.show_date_picker, size_hint_y=None, height=30)
        self.root.add_widget(self.date_button)

        # Spinner for selecting time
        self.time_spinner = Spinner(text='Select Time', values=['12:00 AM', '01:00 AM', '02:00 AM', '03:00 AM', '04:00 AM',
                                                                '05:00 AM', '06:00 AM', '07:00 AM', '08:00 AM', '09:00 AM',
                                                                '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM',
                                                                '03:00 PM', '04:00 PM', '05:00 PM', '06:00 PM', '07:00 PM',
                                                                '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM'],
                                    size_hint_y=None, height=30)
        self.root.add_widget(self.time_spinner)

        # Button for selecting audio file
        self.audio_button = Button(text='Select Audio', on_press=self.show_audio_chooser, size_hint_y=None, height=30)
        self.root.add_widget(self.audio_button)

        # Button to record and set audio
        self.record_audio_button = Button(text='Record Audio', on_press=self.record_and_set_audio,
                                          size_hint_y=None, height=30)
        self.root.add_widget(self.record_audio_button)

        # Button to add reminder
        add_button = Button(text='Add Reminder', on_press=self.add_reminder)
        self.root.add_widget(add_button)

        # Container for displaying reminders
        self.reminder_container = BoxLayout(orientation='vertical', spacing=10)
        self.root.add_widget(self.reminder_container)

        return self.root

    def show_date_picker(self, instance):
        date_popup = Popup(title='Select Date', size_hint=(None, None), size=(300, 300))
        date_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Add Spinner widgets for day, month, and year
        day_spinner = Spinner(text='Day', values=[str(i) for i in range(1, 32)])
        month_spinner = Spinner(text='Month', values=[str(i) for i in range(1, 13)])
        year_spinner = Spinner(text='Year', values=[str(i) for i in range(2022, 2030)])

        date_layout.add_widget(day_spinner)
        date_layout.add_widget(month_spinner)
        date_layout.add_widget(year_spinner)

        # Button to set the selected date
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

        # FileChooser to select audio file
        file_chooser = FileChooserListView()
        audio_layout.add_widget(file_chooser)

        # Button to set the selected audio file
        set_audio_button = Button(text='Set Audio', on_press=lambda x: self.set_selected_audio(audio_popup, file_chooser.path))

        audio_layout.add_widget(set_audio_button)
        audio_popup.content = audio_layout
        audio_popup.open()

    def set_selected_audio(self, audio_popup, selected_path):
        # Ensure that the selected file has the allowed extension
        allowed_extensions = ['.mp3', '.wav']
        _, file_extension = os.path.splitext(selected_path)

        if file_extension.lower() in allowed_extensions and os.path.isfile(selected_path):
            # Store the selected audio file path in your data structure
            # Modify your data structure to include the audio file information
            # For example, you can add a key 'audio_path' with the selected audio file path
            # reminder_entries.append({
            #     'text': reminder_text,
            #     'note': note_text,
            #     'time': time_text,
            #     'date': date_text,
            #     'audio_path': selected_path
            # })

            audio_popup.dismiss()
        else:
            # Display an error message for invalid file type or non-existent file
            error_message = 'Please select a valid audio file (MP3 or WAV).'
            if not os.path.isfile(selected_path):
                error_message = 'File does not exist.'
            error_popup = Popup(title='Invalid File', content=Label(text=error_message), size_hint=(None, None), size=(300, 150))
            error_popup.open()

        if reminder_entries:
            reminder_entries[-1]['audio_path'] = selected_path

        if audio_popup:
            audio_popup.dismiss()

    def record_and_set_audio(self, instance):
        # Record audio and save it to a WAV file
        audio_file_path = 'recorded_audio.wav'
        self.record_audio(audio_file_path, duration=15)
        self.set_selected_audio(None, audio_file_path)

    def record_audio(self, file_path, duration=15):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        frames = []

        print("Recording...")

        for i in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        print("Finished recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save audio to WAV file
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

    def add_reminder(self, instance):
        reminder_text = self.reminder_input.text
        note_text = self.note_input.text
        time_text = self.time_spinner.text
        date_text = self.date_button.text

        if reminder_text:
            # Create a BoxLayout for each reminder entry
            reminder_entry = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=100)

            # Label for displaying the reminder text
            reminder_label = Label(text=f'Reminder: {reminder_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(reminder_label)

            # Label for displaying the note
            note_label = Label(text=f'Note: {note_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(note_label)

            # Label for displaying the timae
            time_label = Label(text=f'Time: {time_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(time_label)

            # Label for displaying the date
            date_label = Label(text=f'Date: {date_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(date_label)

            # Add the reminder entry to the container
            self.reminder_container.add_widget(reminder_entry)

            # Store the reminder entry in the shared data structure
            reminder_entries.append({
                'text': reminder_text,
                'note': note_text,
                'time': time_text,
                'date': date_text,
                'audio_path': None  # Replace None with the actual audio file path when implemented
            })

            # Clear the input after adding a reminder
            self.reminder_input.text = ''
            self.note_input.text = ''
            self.time_spinner.text = 'Select Time'
            self.date_button.text = ''

            save_reminders(reminder_entries)


if __name__ == '__main__':
    ReminderApp().run()
