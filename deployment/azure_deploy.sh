#!/bin/bash

# Log in to Azure
az login

# Create resource group
az group create --name iot-fire-sys-rg --location francecentral

# Create virtual network
az network vnet create --name iot-fire-sys-vnet --resource-group iot-fire-sys-rg --subnet-name default

# Create public IP for MQTT Broker
az network public-ip create --name mqtt-broker-ip --resource-group iot-fire-sys-rg

# Create virtual machine for MQTT Broker
az vm create --resource-group iot-fire-sys-rg --name mqtt-broker-vm --image UbuntuLTS --size Standard_B1s --public-ip-address mqtt-broker-ip --generate-ssh-keys

# Connect to the VM and install Mosquitto
az vm run-command invoke --command-id RunShellScript --name mqtt-broker-vm --resource-group iot-fire-sys-rg --scripts @mosquitto_deploy.sh

# Create virtual machine for Backend API
az vm create --resource-group iot-fire-sys-rg --name backend-api-vm --image UbuntuLTS --size Standard_B1s --public-ip-address --generate-ssh-keys

# Connect to the VM and install Backend API
az vm run-command invoke --command-id RunShellScript --name backend-api-vm --resource-group iot-fire-sys-rg --scripts @backend_deploy.sh

# Finish deployment
echo "Deployment completed!"
