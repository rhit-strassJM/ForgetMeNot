import collections
import datetime
import math

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Color, Line, Rectangle

from time import asctime

Builder.load_string('''
<MyClockWidget>:
    on_pos: self.update_clock()
    on_size: self.update_clock()
    
    canvas.before:
        Color:
            rgb: 1, 1, 1  # Set the background color to white
        Rectangle:
            pos: self.pos
            size: self.size
    
    FloatLayout
        id: face
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.54}
        size: 0.9*min(root.size), 0.9*min(root.size)
        canvas:
            Color:
                rgb: 0.9, 0.8, 0.7
            Ellipse:
                size: self.size
                pos: self.pos
    FloatLayout
        id: hands
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)
''')

Position = collections.namedtuple('Position', 'x y')


class MyClockWidget(FloatLayout):

    digital_clock = Label(
        text=asctime(),
        pos_hint={
            "center_x": 0.5,
            "center_y": -0.05,
        },
        font_size=20,
        color=(0, 0, 0, 1),
    )

    def on_parent(self, myclock, parent):
        """
        Add number labels when added in widget hierarchy
        """
        for i in range(1, 13):
            number = Label(
                text=str(i),
                pos_hint={
                    # pos_hint is a fraction in range (0, 1)
                    "center_x": 0.5 + 0.45*math.sin(2 * math.pi * i/12),
                    "center_y": 0.5 + 0.45*math.cos(2 * math.pi * i/12),
                },
                color = (0, 0, 0)
            )
            self.ids["face"].add_widget(number)
        self.ids["face"].add_widget(self.digital_clock)

    def position_on_clock(self, fraction, length):
        """
        Calculate position in the clock using trygonometric functions
        """
        center_x = self.size[0]/2
        center_y = self.size[1]/2
        return Position(
            center_x + length * math.sin(2 * math.pi * fraction),
            center_y + length * math.cos(2 * math.pi * fraction),
        )

    def update_clock(self, *args):
        """
        Redraw clock hands and update digital clock text
        """
        time = datetime.datetime.now()
        hands = self.ids["hands"]
        seconds_hand = self.position_on_clock(time.second/60, length=0.45*hands.size[0])
        minutes_hand = self.position_on_clock(time.minute/60+time.second/3600, length=0.40*hands.size[0])
        hours_hand = self.position_on_clock(time.hour/12 + time.minute/720, length=0.35*hands.size[0])

        hands.canvas.clear()
        with hands.canvas:
            Color(0, 0, 0)
            Line(points=[hands.center_x, hands.center_y, seconds_hand.x, seconds_hand.y], width=1, cap="round")
            Color(0, 0, 0)
            Line(points=[hands.center_x, hands.center_y, minutes_hand.x, minutes_hand.y], width=2, cap="round")
            Color(0, 0, 0)
            Line(points=[hands.center_x, hands.center_y, hours_hand.x, hours_hand.y], width=3, cap="round")

        formatted_time = time.strftime("%A %B %d, %Y      %I:%M %p")
        self.digital_clock.text = formatted_time
        self.digital_clock.color = (0, 0, 0, 1)


class MyApp(App):
    def build(self):
        clock_widget = MyClockWidget()
        # update initially, just after construction of the widget is complete
        Clock.schedule_once(clock_widget.update_clock, 0)
        # then update every second
        Clock.schedule_interval(clock_widget.update_clock, 1)
        return clock_widget


if __name__ == '__main__':
    MyApp().run()