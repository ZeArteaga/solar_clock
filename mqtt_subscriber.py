from kivy.event import EventDispatcher
import paho.mqtt.client as mqtt 
import ast

class MQTTSubscriber(EventDispatcher):
    def __init__(self):
        super(MQTTSubscriber, self).__init__()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log 
        self.client.username_pw_set(username="user1", password="user1")
        self.client.failed_connect = False
        self.color_values = []
        self.prod_values = [] 
        self.cons_values = []
        
        self.register_event_type('on_first_message_received')
        self.first_message_received = False
        self.register_event_type('on_new_data')

    def on_connect(self, client, userdata, flags, return_code, properties=None):
        if return_code == 0:
            print("Connected successfully")
            client.subscribe("test")
            return True;
        else:
            print(f"Could not connect, return code: {return_code}")
            client.failed_connect = True
            return False;


    def on_message(self, client, userdata, message):
        msg_decoded = str(message.payload.decode("utf-8"))
        msg_decoded = ast.literal_eval(msg_decoded)

         # Check if msg_decoded is empty or any of its elements are not lists with exactly 3 elements
        if not msg_decoded or any(len(sublist) != 3 for sublist in msg_decoded):
            print("Invalid message: either empty or not all elements have exactly 3 elements.")
            return

        self.color_values = []
        self.prod_values = []
        self.cons_values = []
        for sublist in msg_decoded:
            self.color_values.append(sublist[0])
            self.cons_values.append(float(sublist[1]))
            self.prod_values.append(float(sublist[2]))

        #leave blocked mode
        if(not self.first_message_received):
            print("First message received!")
            self.first_message_received = True
            self.dispatch('on_first_message_received')

        print("Received: Color Values: ", self.color_values, "\nProduction Values: ", self.prod_values, "\nConsumption Values: ", self.cons_values)
        self.dispatch('on_new_data')
        
    def on_log(self, client, userdata, level, buf):
        print(f"log: {buf}")

    def connect(self, broker_hostname, port, keep_alive):
        try:
            res = self.client.connect(broker_hostname, port, keep_alive)
            print("MQTT connect call initiated")
            print("Connection result:", res)
            return True
        except Exception as e:
            print(f"Failed to initiate connection to broker: {e}")
            self.failed_connect = True
            return False

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
        
    def on_first_message_received(self):
        pass
    
    def on_new_data(self):
        pass

    def get_color_values(self):
        return self.color_values
    
    def get_prod_values(self):
        return self.prod_values
    
    def get_cons_values(self):
        return self.cons_values    