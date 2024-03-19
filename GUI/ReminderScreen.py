from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView

from kivymd.uix.pickers import MDDatePicker, MDTimePicker
import os
import pyaudio
import wave
import json

class ReminderScreen(Screen):
    name = 'reminder'

    def __init__(self, **kwargs):
        super(ReminderScreen, self).__init__(**kwargs)
        # Create layout
        self.layout = BoxLayout(orientation='vertical')

        # Add title label
        self.title_label = Label(text='Reminder', font_size=30)
        self.layout.add_widget(self.title_label)

        # Add note input field
        self.note_input = TextInput(hint_text='Enter Note')
        self.layout.add_widget(self.note_input)

        # Add buttons for date, time, save, and record audio
        self.date_button = Button(text='Select Date')
        self.date_button.bind(on_press=self.show_date_picker)
        self.time_button = Button(text='Select Time')
        self.time_button.bind(on_press=self.show_time_picker)
        self.add_audio_button = Button(text='Add Audio')
        self.add_audio_button.bind(on_press=self.show_audio_popup)
        self.record_audio_button = Button(text='Record Audio')
        self.record_audio_button.bind(on_press=self.record_audio_wrapper)
        self.save_button = Button(text='Save Reminder')
        self.save_button.bind(on_press=self.save_reminder)

        self.layout.add_widget(self.date_button)
        self.layout.add_widget(self.time_button)
        self.layout.add_widget(self.add_audio_button)
        self.layout.add_widget(self.record_audio_button)
        self.layout.add_widget(self.save_button)

        # Add layout to screen
        self.add_widget(self.layout)

    def on_cancel(self, instance, value):
        print("cancelled")

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def show_time_picker(self, instance):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save, on_cancel=self.on_cancel)
        time_dialog.open()

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

    def record_audio_wrapper(self, instance):
        popup = Popup(title='Recording Audio', size_hint=(0.9, 0.5))
        popup.open()
        record_audio('recorded_audio.wav', popup.dismiss)

    def on_date_save(self, instance, value, date_range):
        global date
        date = value.strftime('%Y-%m-%d')

    def on_time_save(self, instance, value):
        global time
        time = value.strftime('%H:%M')

    def save_reminder(self, instance):
        note = self.note_input.text

        # Here you can save the reminder with the provided information
        print(f"Reminder saved: Date - {date}, Time - {time}, Note - {note}")

# Record audio using PyAudio
def record_audio(file_name, callback, duration=15):
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

    # Save audio to WAV file in the "Recordings" folder
    directory = "Recordings"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    # Call the provided callback function after recording is finished
    if callback:
        callback()

# Convert audio to JSON
def audio_to_json(file_name):
    directory = "Recordings"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Create a dictionary to store audio data
    audio_dict = {
        'sample_rate': 44100,
        'channels': 1,
        'audio_data': audio_data.hex()
    }

    # Convert dictionary to JSON
    json_data = json.dumps(audio_dict)

    # Save JSON data to a file
    json_file_name = os.path.splitext(file_name)[0] + '.json'
    json_file_path = os.path.join(directory, json_file_name)
    with open(json_file_path, 'w') as json_file:
        json_file.write
