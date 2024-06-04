
# - [] setup MQTT connection
# - [] Read data from the sensor
# - [] Send data to the cloud

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.on_connect = on_connect

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor-data")
    
client.connect("mqtt.pervasive.org", 1883, 60)

