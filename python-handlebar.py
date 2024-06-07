# - [] subscribe to MQTT topic
# - [] control LEDs based on MQTT messages
# - [] play sound based on MQTT messages

import paho.mqtt.client as mqtt
# import numpy as np
import RPi.GPIO as GPIO
from time import sleep 
import smart_city


# Define the MQTT broker details
broker = "rasp-wheel"  # Replace with the IP address of your MQTT broker (server Raspberry Pi)
port = 8080           # Default MQTT port
topic = "smartbike"  # Replace with the topic you are subscribing to
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Message received: {message} on topic {msg.topic}")
    
    if message == smart_city.Messages.CHEAT_DETECTED:
        cheating()
    elif "reward" in message:
        turn_on_light()

def turn_on_light():
    GPIO.output(21, GPIO.HIGH)
    sleep(1)
    GPIO.output(21, GPIO.LOW)

def cheating():
    for x in range(8):
        GPIO.output(21, GPIO.HIGH)
        sleep(.2)
        GPIO.output(21, GPIO.LOW)
        sleep(.2)

    
turn_on_light()

# Create an MQTT client instance
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Start the loop to process received messages
client.loop_forever()
