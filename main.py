from os import environ
import sys
environ['DISPLAY'] = ':0' #set to local display
 
from kivy.app import App
from kivy.app import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.properties import ListProperty
from kivy.clock import mainthread
from controllers.homescreen import Screen_Home
from controllers.mode_hourly import Screen_Hourly 
from controllers.blocked_screen import Screen_Blocked    
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
        Builder.load_file("views/blocked_screen.kv")

        LabelBase.register(name="Aptos",
                   fn_regular="assets/fonts/aptos/aptos.ttf",
                   fn_bold="assets/fonts/aptos/aptos-bold.ttf",
                   fn_italic="assets/fonts/aptos/aptos-italic.ttf"
                   )           

        self.sm = ScreenManager(transition=FadeTransition())
        self.mqtt_client = MQTTSubscriber()
        self.mqtt_client.client.on_disconnect = self.on_disconnect

        self.sm.add_widget(Screen_Blocked(name='blocked', mqtt_client=self.mqtt_client))
        self.sm.add_widget(Screen_Hourly(name='hourly', app=self, mqtt_client=self.mqtt_client))
        self.sm.add_widget(Screen_Home(name='homescreen'))

        return self.sm
    
    @mainthread
    def on_disconnect(self, client, userdata, rc):
        print("Disconnected, reverting to blocked screen")
        self.mqtt_client.loop_stop()
        self.sm.current = 'blocked'
        

if __name__ == '__main__':
    app = SolarClock()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Application interrupted, stopping MQTT loop")
        app.mqtt_client.loop_stop()
        app.mqtt_client.disconnect()
        sys.exit(0)
    