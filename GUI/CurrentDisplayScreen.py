import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

SCOPES = ['https://www.googleapis.com/auth/drive']


Builder.load_string('''
<CurrentDisplayScreen>:
    canvas.before:
        Color:
            rgb: 0.820, 0.925, 1
        Rectangle:
            pos: self.pos
            size: self.size
''')


class CurrentDisplayScreen(Screen):
    name = 'display'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        folder_id = '187UAKNesq0U0FA6E043aP-JnTKGixDhA'

        # Create a vertical BoxLayout to hold the buttons and another layout
        layout = BoxLayout(orientation='vertical')

        # Create a horizontal BoxLayout for the row of buttons
        button_row = BoxLayout(orientation='horizontal')

        # Add some spacing to push the buttons to the bottom of the screen
        layout.add_widget(BoxLayout(size_hint_y=0.99))

        add_alarm_button = Button(text="Add Alarm", size_hint=(0.5, 1), on_press=self.add_alarm, background_color=[0.475, 0.655, 0.784])
        add_image_button = Button(text="Add Image", size_hint=(0.5, 1), on_press=lambda instance: self.show_image_popup(folder_id), background_color=[0.475, 0.655, 0.784])

        # Add buttons to the button_row layout
        button_row.add_widget(add_alarm_button)
        button_row.add_widget(add_image_button)

        # Add the button_row to the main layout
        layout.add_widget(button_row)



        # Add the main layout to the screen
        self.add_widget(layout)

    def show_image_popup(self, folder_id):
        popup = AddImagePopup(folder_id=folder_id)
        popup.open()

    def add_alarm(self, instance):
        print("Add Alarm button clicked")
        App.get_running_app().show_current_reminder_screen()

class AddImagePopup(Popup):
    def __init__(self, folder_id, **kwargs):
        super(AddImagePopup, self).__init__(**kwargs)
        self.folder_id = folder_id
        self.title = 'display'
        self.file_chooser = FileChooserListView(path='.')
        self.file_chooser.bind(on_submit=self.upload_image)
        self.add_widget(self.file_chooser)

    def upload_image(self, instance, value, *args):
        image_path = value[0]
        credentials = self.get_credentials()
        if credentials:
            service = build('drive', 'v3', credentials=credentials)
            file_metadata = {
                'name': os.path.basename(image_path),
                'parents': [self.folder_id]  # Specify the parent folder's ID
            }
            media = MediaFileUpload(image_path, mimetype='image/jpeg')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print('File ID:', file.get('id'))
            self.dismiss()

    def get_credentials(self):
        credentials = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json')
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
        return credentials
