from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from GUI.data_manager import reminder_entries, save_reminders
from kivy.uix.screenmanager import Screen


class ReminderApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Entry Boxes for Reminder, Note, and Time
        self.reminder_input = TextInput(hint_text='Enter Reminder', multiline=False, size_hint_y=None, height=30)
        self.note_input = TextInput(hint_text='Add a Note', multiline=False, size_hint_y=None, height=30)
        self.time_input = TextInput(hint_text='Set Time', multiline=False, size_hint_y=None, height=30)

        entry_box = BoxLayout(orientation='horizontal', spacing=10)
        entry_box.add_widget(self.reminder_input)
        entry_box.add_widget(self.note_input)
        entry_box.add_widget(self.time_input)

        self.root.add_widget(entry_box)
        print("hi guys")

        # Button to add reminder
        add_button = Button(text='Add Reminder', on_press=self.add_reminder)
        self.root.add_widget(add_button)

        # Container for displaying reminders
        self.reminder_container = BoxLayout(orientation='vertical', spacing=10)
        self.root.add_widget(self.reminder_container)

        return self.root

    def add_reminder(self, instance):
        reminder_text = self.reminder_input.text
        note_text = self.note_input.text
        time_text = self.time_input.text

        if reminder_text:
            # Create a BoxLayout for each reminder entry
            reminder_entry = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=100)

            # Label for displaying the reminder text
            reminder_label = Label(text=f'Reminder: {reminder_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(reminder_label)

            # Label for displaying the note
            note_label = Label(text=f'Note: {note_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(note_label)

            # Label for displaying the time
            time_label = Label(text=f'Time: {time_text}', size_hint_y=None, height=30)
            reminder_entry.add_widget(time_label)

            # Add the reminder entry to the container
            self.reminder_container.add_widget(reminder_entry)

            # Store the reminder entry in the shared data structure
            reminder_entries.append({
                'text': reminder_text,
                'note': note_text,
                'time': time_text
            })

            # Clear the input after adding a reminder
            self.reminder_input.text = ''
            self.note_input.text = ''
            self.time_input.text = ''

            save_reminders(reminder_entries)


if __name__ == '__main__':
    ReminderApp().run()