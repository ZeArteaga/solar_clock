from os import environ
environ['DISPLAY'] = ':0' #set to local display
 
from kivy.app import App
from kivy.app import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from controllers.homescreen import Screen_Home
from controllers.mode_hourly import Screen_Hourly 
from controllers.blocked_screen import Screen_Blocked    
from kivy.properties import ListProperty
from mqtt_subscriber import MQTTSubscriber

class SolarClock(App):

    rgba_green = ListProperty([0.5,1,0.5,1])
    rgba_yellow = ListProperty([1,1,0,1])
    rgba_red = ListProperty([1,0.5,0.5,1])
    rgba_blue = ListProperty([0.678,0.847,0.902,1])

    def build(self):
        Window.maximize()
        Window.borderless = True

        Builder.load_file("widgets/clock.kv") 
        Builder.load_file("views/common.kv")
        Builder.load_file("views/homescreen.kv") 
        Builder.load_file("views/mode_hourly.kv")

        LabelBase.register(name="Aptos",
                   fn_regular="assets/fonts/aptos/aptos.ttf",
                   fn_bold="assets/fonts/aptos/aptos-bold.ttf",
                   fn_italic="assets/fonts/aptos/aptos-italic.ttf"
                   )           

        self.sm = ScreenManager(transition=FadeTransition())
        self.mqtt_client = MQTTSubscriber()
        screen_blocked = Screen_Blocked(name='blocked', mqtt_client = self.mqtt_client)
        self.sm.add_widget(screen_blocked)
        self.sm.add_widget(Screen_Hourly(name='hourly'))
        self.sm.add_widget(Screen_Home(name='homescreen'))
        
        

        return self.sm

if __name__ == '__main__':
    SolarClock().run()