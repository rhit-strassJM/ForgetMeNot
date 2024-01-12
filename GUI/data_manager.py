# GUI/data_manager.py
import json

def save_reminders(reminder_entries):
    with open('reminders.json', 'w') as file:
        json.dump(reminder_entries, file)

def load_reminders():
    try:
        with open('reminders.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

reminder_entries = load_reminders()