
# - [] setup MQTT connection
# - [] Read data from the sensor
# - [] Send data to the cloud

import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import time
import dotenv
import os
import pandas as pd
import math
import smart_city

dotenv.load_dotenv('.env')

url = os.getenv('MQTT_URL')
topic = os.getenv('TOPIC')

magnet_threshold = 75
wheel_circumference = 0.5 # meters
reward_distance = 5 # 5 for testing
reward_points = 1

rewards = 0
distance = 0
temp_distance = 0.0 #used for calculating the rewards
total_distance = 0

last_bike_movement: pd.Timestamp = pd.Timestamp(0)

sense = SenseHat()


def on_connect(client, userdata, flags, rc):
	client.subscribe(topic, qos=0)
    

client = mqtt.Client()
client.on_connect = on_connect

client.connect(os.getenv('BROKER_HOST'), int(os.getenv('BROKER_PORT')), 60)

last_magnet_detected = False
start_time = time.time()


while True:
    current_time = time.time()
    magnetometer = sense.get_compass_raw()
    accelerometer = sense.get_accelerometer_raw()
    
    
    mag_x = magnetometer['x']
    mag_y = magnetometer['y']
    mag_z = magnetometer['z']
    
    magnet_strength = (mag_x**2 + mag_y**2 + mag_z**2)**0.5

    # Accelerometer bike movement 
    acc_x, acc_y, acc_z = accelerometer['x'], accelerometer['y'], accelerometer['z']
    bike_movement = (acc_x**2 + acc_y**2 + acc_z**2)**0.5
    
                

    # Check if the magnet is close
    if magnet_strength > magnet_threshold and not last_magnet_detected:
        rotation_time = current_time - last_detection_time
        last_detection_time = current_time

        if last_rotation_time > 0:
            # change in rotation times represents a relative change in speed
            speed_change = abs(rotation_time - last_rotation_time) / last_rotation_time 
            speed_m_s = wheel_circumference / rotation_time

            # Verify with accelerometer if there is a significant speed change
            if speed_change > 0.1:  # Assume 10% change as significant
                acceleration = sense.get_accelerometer_raw()
                accel_x = acceleration['x']
                accel_y = acceleration['y']
                accel_z = acceleration['z']
                current_acceleration = math.sqrt(accel_x**2 + accel_y**2 + accel_z**2)

                print(f"Significant speed change detected: {speed_change*100:.2f}%")
                print(f"Acceleration magnitude at time of detection: {current_acceleration:.2f} m/s²")
                client.publish(topic, f"Change: {speed_change*100:.2f}%, Accel: {current_acceleration:.2f} m/s²")
                
                client.publish(topic, f"speed_m_s: {speed_m_s:.2f} m/s")

                if current_acceleration > 1.5:
                    print("Bike movement detected")
                    client.publish(topic, smart_city.Messages.MOVEMENT_DETECTED)
                    last_bike_movement = pd.Timestamp.now()
                else:
                    print("No bike movement detected: cheater!")
                    client.publish(topic, smart_city.Messages.CHEAT_DETECTED)

        last_rotation_time = rotation_time
        distance += wheel_circumference
        total_distance += wheel_circumference
        print(f"Magnet detected! Distance this session: {distance:.2f} meters")
        last_magnet_detected = True


    elif magnet_strength <= magnet_threshold:
        last_magnet_detected = False

    if temp_distance >= reward_distance:
        rewards += reward_points
        print("Sending update. Total distance: {:.2f} meters".format(distance))
        client.publish(topic, payload=smart_city.Messages.REWARD(reward_points))
        temp_distance -= reward_distance  # Reset session distance


    # Print sensor data every .1 second for debugging
    if time.time() - start_time >= .1:
        print("Current readings: x={:7.2f}, y={:7.2f}, z={:7.2f}, strength={:7.2f}".format(mag_x, mag_y, mag_z, magnet_strength))
        start_time = time.time()
        

    
    