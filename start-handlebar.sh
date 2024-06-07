#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' /home/pi/embedded-2024/.env | xargs)


# no flag
if [ -z "$1" ]; then
    echo "No flag provided"
    exit 1
fi


# run python flag
if [ "$1" == "--run" ]; then
    echo "Run python program"
    python $PYTHON_HANDLEBAR
    exit 0
fi
