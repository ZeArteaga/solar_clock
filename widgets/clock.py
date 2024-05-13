from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, OptionProperty, NumericProperty
from kivy.clock import Clock
from datetime import datetime

class ClockWidget(BoxLayout):
    
    label_alignment = OptionProperty('center', options=['left', 'center', 'right'])
    current_time = StringProperty()
    todays_date = StringProperty()
    time_fontsize = NumericProperty()
    date_fontsize = NumericProperty()

    def __init__(self, **kwargs):
        super(ClockWidget, self).__init__(**kwargs)
                
        self.current_time = datetime.now().strftime('%H:%M')
        self.todays_date = datetime.now().strftime('%A, %B %d')
        Clock.schedule_interval(self.update_clock, 1) #update clock every second, not very efficient but whatever

    def update_clock(self, dt):
        #print(dt) to check the callback time ~ 1s
        
        if(self.current_time != datetime.now().strftime('%H:%M')):
            self.current_time = datetime.now().strftime('%H:%M')
                                                        
        if(self.todays_date != datetime.now().strftime('%A, %B %d')):
            self.todays_date = datetime.now().strftime('%A, %B %d')
            