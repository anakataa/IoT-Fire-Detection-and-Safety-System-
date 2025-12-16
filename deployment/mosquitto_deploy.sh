#!/bin/bash

# Update and install Mosquitto MQTT Broker
sudo apt update
sudo apt install -y mosquitto mosquitto-clients

# Configure Mosquitto to listen on all interfaces
sudo sed -i '/^#listener 1883/ a listener 1883\nallow_anonymous true' /etc/mosquitto/mosquitto.conf

# Restart Mosquitto service
sudo systemctl restart mosquitto

# Check Mosquitto service status
sudo systemctl status mosquitto
