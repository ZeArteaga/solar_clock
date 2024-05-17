from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.app import App
from kivy.clock import Clock

class Screen_Hourly(Screen):
    pass

class RectStack(BoxLayout):
    def __init__(self, **kwargs):
        super(RectStack, self).__init__(**kwargs)
        
        self.app = App.get_running_app()
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

        Clock.schedule_interval(self.update_hour, 1)        
    
    def update_hour(self, dt):
        #get clock widget from screen instance
        curr_hour = int(self.parent.ids.clock.current_time[0:2])
        if(curr_hour != self.index_high):
            self.switch_highlight(self.index_high, curr_hour)

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
              