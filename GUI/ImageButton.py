from kivy.uix.image import Image

class ImageButton(Image):
    def __init__(self, screen_manager, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.screen_manager = screen_manager

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.source == 'ButtonImages/AddAlarm.png':
                # Access the ScreenManager instance and switch to a new screen
                self.screen_manager.current = 'login'
            else:
                print(f"{self.source} button pressed")
            return True  # consume the touch event
        return super().on_touch_down(touch)
