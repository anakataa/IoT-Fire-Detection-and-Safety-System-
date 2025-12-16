# IoT

## Project Overview

This is an IoT system using cloud computing technologies. The project includes:

- **MQTT Broker** for data exchange between IoT devices and the cloud.
- **PostgreSQL** for data storage.
- **Backend API** for business logic.

## Requirements

- **Java 17** for Backend API.
- **PostgreSQL** for database management.
- **Mosquitto** for MQTT Broker.
- **Azure** for cloud deployment.

## Installation

### Step 1: Deploy MQTT Broker (Mosquitto)

Download and extract the Mosquitto deployment script:

```bash
./mosquitto_deploy.sh
```

### Step 2: Deploy PostgreSQL

Install PostgreSQL:

```bash
./postgresql_deploy.sh
```

### Step 3: Deploy Backend API

Clone the repository and run the Backend API:

```bash
./backend_deploy.sh
```

Deploying to Azure

To deploy the project to Azure, use the following script:

```bash
./azure_deploy.sh
```
