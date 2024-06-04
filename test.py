# - [] subscribe to MQTT topic
# - [] control LEDs based on MQTT messages
# - [] play sound based on MQTT messages

import paho.mqtt.client as mqtt
import pyaudio
import numpy as np
import sounddevice as sd

frequency = 440  # Frequency of the tone
fs = 44100  # Sampling rate
seconds = 1  # Duration of the tone

# Generate the sound wave
t = np.linspace(0, seconds, seconds * fs, False)
note = np.sin(frequency * t * 2 * np.pi)

# Ensure that highest value is in 16-bit range
audio = note * (2**15 - 1) / np.max(np.abs(note))
# Convert to 16-bit data
audio = audio.astype(np.int16)

# Play the audio
sd.play(audio, fs)
sd.wait()  # Wait until the sound has finished playing