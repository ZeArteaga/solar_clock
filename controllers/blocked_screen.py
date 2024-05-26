from kivy.uix.screenmanager import Screen
from kivy.clock import Clock, mainthread

class Screen_Blocked(Screen):
    def __init__(self, mqtt_client, **kwargs):
        super(Screen_Blocked, self).__init__(**kwargs)
        self.mqtt_client = mqtt_client
        self.mqtt_client.bind(on_first_message_received=self.leave)
        
    def on_enter(self):
        self.attempt_reconnect(0)  # Start the reconnection attempts immediately

    def attempt_reconnect(self, dt):
        self.message = "Connecting..."
        success = self.mqtt_client.connect(broker_hostname="192.168.29.113", port=1883, keep_alive=60)
        if success:
            self.message = "Connected!"
            # If connection successful, start the MQTT client loop
            self.mqtt_client.loop_start()
            # if data has already been received before 
            if self.mqtt_client.first_message_received:
                self.leave()
            else:
                self.message = "Waiting for data..."
        else:
            # If connection failed, schedule another attempt in 5 seconds
            Clock.schedule_once(self.attempt_reconnect, 5)

    @mainthread
    def leave(self, *args):
        self.manager.current = 'hourly'