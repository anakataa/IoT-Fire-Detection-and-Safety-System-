#!/bin/bash

# Install PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE iot_data;
CREATE USER iot WITH PASSWORD 'iotpass';
GRANT ALL PRIVILEGES ON DATABASE iot_data TO iot;
EOF

# Check PostgreSQL service status
sudo systemctl status postgresql
