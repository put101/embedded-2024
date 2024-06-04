#!/bin/bash

export PROJECT_DIR=/home/pi/embedded-2024
cd $PROJECT_DIR

# Start MQTT broker service
mosquitto -c mosquitto.conf
pid=$!
sleep 5
echo "MQTT broker started with PID: $pid"

# Start the wheel service
python python_script.py &
python_pid=$!
echo "Wheel service started with PID: $python_pid"

