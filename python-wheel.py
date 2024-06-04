
# - [] setup MQTT connection
# - [] Read data from the sensor
# - [] Send data to the cloud

import paho.mqtt.client as mqtt
  

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor-data")
    
    
