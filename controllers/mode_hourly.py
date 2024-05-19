from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.app import App
from kivy.clock import Clock

RESET_CLOCK_TIME = 2

class Screen_Hourly(Screen):
    def __init__(self, **kwargs):
        super(Screen_Hourly, self).__init__(**kwargs)
        self.inactivity_timer = None
        self.reset_time = RESET_CLOCK_TIME

    def increment_hour(self):
        self.ids.clock.increment_hour()
        self.trigger_inactivity_timer()

    def decrement_hour(self):
        self.ids.clock.decrement_hour()
        self.trigger_inactivity_timer()

    def trigger_inactivity_timer(self):
        if self.inactivity_timer:
            Clock.unschedule(self.inactivity_timer)
        #call update to current time in reset_time seconds
        self.inactivity_timer = Clock.schedule_once(self.ids.clock.reschedule_time_event, self.reset_time)

class RectStack(BoxLayout):
    def __init__(self, **kwargs):
        super(RectStack, self).__init__(**kwargs)
        
        self.rectangles = []
        self.index_high = 0 
        self.lower_rect_y = 0.6

        for h in range(24):
            rect = RectangleWidget("None") #insert color data here
            self.add_widget(rect)
            self.rectangles.append(rect)
            if(h != self.index_high):
                rect.size_hint_y = self.lower_rect_y #non highlighted
            else:
                rect.size_hint_y = 1    #highlight pos=0 in init
    
    def update_hour(self, displayed_time):
        #get clock widget from screen instance
        disp_hour = int(displayed_time[0:2])
        if(disp_hour != self.index_high):
            self.switch_highlight(self.index_high, disp_hour)

    def switch_highlight(self, old_index, new_index): 
        old_rect = self.rectangles[old_index]
        new_rect = self.rectangles[new_index]
        new_rect.size_hint_y = 1 #raise new
        old_rect.size_hint_y = self.lower_rect_y  #reset old
        self.index_high = new_index

class RectangleWidget(Widget):   
    rect_color = ListProperty()
    
    def __init__(self, color, **kwargs):
        super(RectangleWidget, self).__init__(**kwargs)
        
        app = App.get_running_app()
        if(color == "green"):
            self.rect_color = app.rgba_green
        elif(color == "yellow"):
            self.rect_color = app.rgba_yellow
        elif(color == "red"):
            self.rect_color = app.rgba_red
        elif(color == "blue"):
            self.rect_color = app.rgba_blue
        else:
            self.rect_color = [1,1,1,1] #white
              