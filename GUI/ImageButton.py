from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from google.oauth2 import service_account
from googleapiclient.discovery import build

class ImageButton(Image):
    def __init__(self, screen_manager, folder_id, json_key_file, file_chooser_popup, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.folder_id = folder_id
        self.json_key_file = json_key_file
        self.file_chooser_popup = file_chooser_popup
        self.file_chooser = FileChooserListView()
        self.file_chooser.bind(on_submit=self.upload_to_drive)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.source == 'ButtonImages/AddAlarm.png':
                # Access the ScreenManager instance and switch to a new screen
                self.screen_manager.current = 'reminder'
            else:
                # Show file chooser popup when Add Photo button is pressed
                if self.source == 'ButtonImages/AddImage.png':
                    self.file_chooser_popup.open()
                else:
                    print(f"{self.source} button pressed")
            return True  # consume the touch event
        return super().on_touch_down(touch)

    def upload_to_drive(self, instance, selection, touch):
        if selection:
            selected_file = selection[0]  # Assuming only one file is selected
            credentials = service_account.Credentials.from_service_account_file(self.json_key_file)
            drive_service = build('drive', 'v3', credentials=credentials)

            file_metadata = {'name': os.path.basename(selected_file), 'parents': [self.folder_id]}
            media = {'mimeType': 'image/jpeg', 'body': open(selected_file, 'rb')}
            try:
                uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print('File ID:', uploaded_file.get('id'))
                print('Image uploaded successfully!')
                self.file_chooser_popup.dismiss()
            except Exception as e:
                print(f"Error uploading file: {e}")
