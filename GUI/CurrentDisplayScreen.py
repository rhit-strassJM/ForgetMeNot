import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen

SCOPES = ['https://www.googleapis.com/auth/drive']

class CurrentDisplayScreen(Screen):
    name = 'display'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        folder_id = '187UAKNesq0U0FA6E043aP-JnTKGixDhA'  # Replace 'your_folder_id' with the actual folder ID
        self.add_widget(Button(text="Add Image", on_press=lambda instance: self.show_image_popup(folder_id)))

    def show_image_popup(self, folder_id):
        popup = AddImagePopup(folder_id=folder_id)
        popup.open()

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
