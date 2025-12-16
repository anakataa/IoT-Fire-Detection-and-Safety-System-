#!/bin/bash

# Install JDK (if not installed)
sudo apt update
sudo apt install -y openjdk-17-jdk

# Build and run the application
./gradlew clean build
java -jar build/libs/your-backend-api.jar &

# Check the health of the service
curl http://localhost:8081/health
