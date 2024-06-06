#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' /home/pi/embedded-2024/.env | xargs)


# no flag
if [ -z "$1" ]; then
    echo "No flag provided"
    exit 1
fi

# kill flag
if [ "$1" == "--kill" ]; then
    echo "Kill mosquitto"
    pkill -f "mosquitto -c $PROJECT_DIR/$CONFIG_FILE"
    exit 0
fi


# Start mosquitto flag
if [ "$1" == "--start" ]; then
    echo "Starting mosquitto"
    mosquitto -c $PROJECT_DIR/$CONFIG_FILE >> $LOG_FILE 2>&1 &
    
    if [ $? -ne 0 ]; then
      echo "Failed to start mosquitto"
    fi
    exit 0
fi

sleep 1

# run python flag
if [ "$1" == "--run" ]; then
    echo "Run python program"
    python $PYTHON_WHEEL
    exit 0
fi
