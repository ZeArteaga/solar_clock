from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, OptionProperty, NumericProperty
from kivy.clock import Clock
from datetime import datetime
from kivy.event import EventDispatcher

class ClockWidget(BoxLayout, EventDispatcher):
    
    label_alignment = OptionProperty('center', options=['left', 'center', 'right'])
    displayed_time = StringProperty()
    todays_date = StringProperty()
    time_fontsize = NumericProperty()
    date_fontsize = NumericProperty()
    event_disp_time = None

    def __init__(self, **kwargs):
        super(ClockWidget, self).__init__(**kwargs)
                
        self.reschedule_time_event()
        Clock.schedule_interval(self.set_to_current_date, 1)

    def set_to_current_time(self, dt):
        #print(dt) to check the callback time ~ 1s
        if(self.displayed_time != datetime.now().strftime('%H:%M')):
            self.displayed_time = datetime.now().strftime('%H:%M')
    
    def set_to_current_date(self, dt):                                                   
        if(self.todays_date != datetime.now().strftime('%A, %B %d')):
            self.todays_date = datetime.now().strftime('%A, %B %d')

    def increment_hour(self):
        self.unschedule_time_event()
        self.displayed_time = str((int(self.displayed_time[:2]) + 1) % 24).zfill(2) + ":--"

    def decrement_hour(self):
        self.unschedule_time_event()
        self.displayed_time = str((int(self.displayed_time[:2]) - 1) % 24).zfill(2) + ":--"

    def reschedule_time_event(self, dt=None):
        if(self.event_disp_time is None): #if unscheduled
            self.event_disp_time = Clock.schedule_interval(self.set_to_current_time, 1)

    def unschedule_time_event(self):
        if(self.event_disp_time is not None):
            Clock.unschedule(self.event_disp_time)
            self.event_disp_time = None        
      