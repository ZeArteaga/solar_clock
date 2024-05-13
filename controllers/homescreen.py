from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime

class Screen_Home(Screen):
    pass

class Home(BoxLayout):
    pass

class Home_Modes(BoxLayout):
    pass

class Header(BoxLayout):
    current_time = StringProperty()
    todays_date = StringProperty()

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)

        self.current_time = datetime.now().strftime('%H:%M')
        self.todays_date = datetime.now().strftime('%A, %B %d')
        Clock.schedule_interval(self.update_clock, 1) #update clock every second, not very efficient but whatever

    def update_clock(self, dt):
        #print(dt) to check the callback time ~ 1s
        
        if(self.current_time != datetime.now().strftime('%H:%M')):
            self.current_time = datetime.now().strftime('%H:%M')
                                                        
        if(self.todays_date != datetime.now().strftime('%A, %B %d')):
            self.todays_date = datetime.now().strftime('%A, %B %d')
           