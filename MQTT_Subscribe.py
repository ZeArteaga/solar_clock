import paho.mqtt.client as mqtt 
import time
import ast

def on_connect(client, userdata, flags, return_code, properties=None):
    if return_code == 0:
        print("Connected successfully")
        client.subscribe("test")
    else:
        print(f"Could not connect, return code: {return_code}")
        client.failed_connect = True

def on_message(client, userdata, message):
    all_values = str(message.payload.decode("utf-8"))
    all_values = ast.literal_eval(all_values)
    pie_values = []
    production_values = []
    consumption_values = []

    for sublist in all_values:
        if len(sublist) == 3:
            pie_values.append(sublist[0])
            production_values.append(sublist[1])
            consumption_values.append(sublist[2])
        else:
            print(f"Warning: The list '{sublist}' does not have exactly 3 elements")
    
    print("Pie Values: ", pie_values, "\nProduction Values: ", production_values, "\nConsumption Values: ", consumption_values)
    # return pie_values, production_values, consumption_values

def on_log(client, userdata, level, buf):
    print(f"log: {buf}")

broker_hostname = "172.21.5.47"
port = 1883 

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log 

client.username_pw_set(username="user1", password="user1")
client.connect(broker_hostname, port, 60)

client.failed_connect = False

client.loop_start()

# This try-finally block ensures that whenever we terminate the program earlier by hitting ctrl+c, it still gracefully exits
try:
    i = 0
    while i < 20 and not client.failed_connect:
        time.sleep(1)
        i += 1
    if client.failed_connect:
        print('Connection failed, exiting...')

finally:
    client.disconnect()
    client.loop_stop()
