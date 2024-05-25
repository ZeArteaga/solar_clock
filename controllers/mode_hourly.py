from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.clock import Clock, mainthread

RESET_CLOCK_TIME = 4

class Screen_Hourly(Screen):
    background_color = ListProperty([1, 1, 1, 1])
    hour_selected = 0
    prod = ListProperty([])
    cons = ListProperty([])

    def __init__(self, app, mqtt_client, **kwargs):
        super(Screen_Hourly, self).__init__(**kwargs)
        self.app = app
        self.mqtt_client = mqtt_client
        self.mqtt_client.bind(on_new_data = self.on_new_data)
        self.inactivity_timer = None
        self.reset_time = RESET_CLOCK_TIME
        self.colors = [[1, 1, 1, 1]] * 24
        self.prod = [0] * 24
        self.cons = [0] * 24

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
    
    def update_hour(self, displayed_time):
        disp_hour = int(displayed_time[0:2])
        if(disp_hour != self.hour_selected):
            self.ids.rect_stack.switch_highlight(self.hour_selected, disp_hour)
            self.background_color = self.colors[disp_hour]
            self.ids.prod_label.value = round(self.prod[disp_hour], 4)
            self.ids.cons_label.value = round(self.cons[disp_hour], 4)
            self.hour_selected = disp_hour

    @mainthread
    def on_new_data(self, args):
        rectangles = self.ids.rect_stack.rectangles
        colors_coded = self.mqtt_client.get_color_values()
        self.prod = self.mqtt_client.get_prod_values()
        self.cons = self.mqtt_client.get_cons_values()

        for h in range(24):
            if colors_coded[h] == 0:
                self.colors[h] = self.app.rgba_green
            elif colors_coded[h] == 1:
                self.colors[h] = self.app.rgba_yellow
            elif colors_coded[h] == 2:
                self.colors[h] = self.app.rgba_red
            elif colors_coded[h] == 3:
                self.colors[h] = self.app.rgba_blue
            rectangles[h].change_color(self.colors[h])
        
        self.background_color = self.colors[self.hour_selected]
        self.ids.prod_label.value = round(self.prod[self.hour_selected], 4)
        self.ids.cons_label.value = round(self.cons[self.hour_selected], 4)

class RectStack(BoxLayout):
    def __init__(self, **kwargs):
        super(RectStack, self).__init__(**kwargs)
        
        self.rectangles = [] 
        self.lower_rect_y = 0.6

        for h in range(24):
            rect = RectangleWidget()
            self.add_widget(rect)
            self.rectangles.append(rect)
            if(h != 0):
                rect.size_hint_y = self.lower_rect_y #non highlighted
            else:
                rect.size_hint_y = 1    #highlight pos=0 in init

    def switch_highlight(self, old_index, new_index): 
        old_rect = self.rectangles[old_index]
        new_rect = self.rectangles[new_index]
        new_rect.size_hint_y = 1 #raise new
        old_rect.size_hint_y = self.lower_rect_y  #reset old

class RectangleWidget(Widget):   
    rect_color = ListProperty([1,1,1,1]) #default color: white
    
    def __init__(self, **kwargs):
        super(RectangleWidget, self).__init__(**kwargs)
            
    def change_color(self, color):
        self.rect_color = color  