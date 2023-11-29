from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MainApp(App):
    def build(self):
        layout = BoxLayout(padding=10)
        #layout.
        btn1 = Button(text =" ",
                     background_normal = 'Images/alarmclock.png',
                     background_down ='Images/alarmclockdown.png',
                     size_hint = (.3, .5),
                     pos_hint = {"x":0, "y":0.5}
                   )
        layout.add_widget(btn1)
        btn1.bind(on_press = self.callback1)

        btn2 = Button(text =" ",
                     background_normal = 'Images/pencil.png',
                     background_down ='Images/pencildown.png',
                     size_hint = (.3, .5),
                   )
        btn2.bind(on_press = self.callback2)
        layout.add_widget(btn2)

        btn3 = Button(text =" ",
                     background_normal = 'Images/calander.png',
                     background_down ='Images/calanderdown.png',
                     size_hint = (.3, .5),
                     #pos_hint = {"x":0.35, "y":0.3}
                   )
        btn3.bind(on_press = self.callback3)
        layout.add_widget(btn3)

        return layout

    def callback1(self, event):
        print("ALARM button pressed")
    def callback2(self, event):
        print("EDIT button pressed")
    def callback3(self, event):
        print("HISTORY button pressed")



if __name__ == '__main__':
    app = MainApp()
    app.run()
