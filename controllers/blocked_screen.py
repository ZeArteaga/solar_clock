from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread

class Screen_Blocked(Screen):
    def __init__(self, mqtt_client, **kwargs):
        super(Screen_Blocked, self).__init__(**kwargs)
        self.mqtt_client = mqtt_client
        self.mqtt_client.bind(on_first_message_received=self.leave)
        
    def on_enter(self):
        success = self.mqtt_client.connect(broker_hostname="192.168.1.69", port=1883, keep_alive=60)
        if success:
            # If connection successful, start the MQTT client loop
            self.mqtt_client.loop_start()
            
            #if had already sent data before 
            if self.mqtt_client.first_message_received:
                self.leave()

    @mainthread
    def leave(self, *args):
        self.manager.current = 'hourly'