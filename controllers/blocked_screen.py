from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread

class Screen_Blocked(Screen):
    def __init__(self, mqtt_client, **kwargs):
        super(Screen_Blocked, self).__init__(**kwargs)
        self.mqtt_client = mqtt_client
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.bind(on_first_message_received=self.leave)
        
    def on_enter(self):
        success = self.mqtt_client.connect(broker_hostname="192.168.1.69", port=1883, keep_alive=60)
        if success:
            # If connection successful, start the MQTT client loop
            self.mqtt_client.loop_start()
        else:
            # If connection failed, revert to the blocked screen
            self.on_disconnect(None, None, None)
 
    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from broker, reverting to blocked screen")
        self.manager.current = 'blocked'    
    
    @mainthread
    def leave(self, *args):
        self.manager.current = 'hourly'