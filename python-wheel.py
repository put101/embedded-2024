
# - [] setup MQTT connection
# - [] Read data from the sensor
# - [] Send data to the cloud

import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import time
import dotenv
import os

dotenv.load_dotenv('.env')

url = os.getenv('MQTT_URL')

magnet_threshold = 75
wheel_circumference = 0.5 # meters

sense = SenseHat()


def on_connect(client, userdata, flags, rc):
	client.subscribe("mymqtttopic", qos=0)
    

client = mqtt.Client()
client.on_connect = on_connect

client.connect(os.getenv('BROKER_HOST'), int(os.getenv('BROKER_PORT')), 60)

distance = 0.0
last_magnet_detected = False
start_time = time.time()

while True:
    magnetometer = sense.get_compass_raw()
    mag_x = magnetometer['x']
    mag_y = magnetometer['y']
    mag_z = magnetometer['z']
    
    magnet_strength = (mag_x**2 + mag_y**2 + mag_z**2)**0.5

    # Check if the magnet is close
    if magnet_strength > magnet_threshold and not last_magnet_detected:
        distance += wheel_circumference
        print("Magnet detected! Total distance: {:.2f} meters".format(distance))
        last_magnet_detected = True


    elif magnet_strength <= magnet_threshold:
        last_magnet_detected = False


    # Print sensor data every second for debugging
    if time.time() - start_time >= .1:
        print("Current readings: x={:7.2f}, y={:7.2f}, z={:7.2f}, strength={:7.2f}".format(mag_x, mag_y, mag_z, magnet_strength))
        start_time = time.time()
