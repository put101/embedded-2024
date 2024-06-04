# Installing relevant tools
```
sudo apt update
sudo apt upgrade -y
```

## Mosquitto
```
sudo apt install -y mosquitto mosquitto-clients
```

Enable the service
```
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

## set git user config
```
git config --global user.name "0xA user"
git config --global user.email "user@0xA.at"
```

## python packages
pip install paho-mqtt

