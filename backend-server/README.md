# 🔥 IoT Fire Detection & Safety System

![Java](https://img.shields.io/badge/Java-17%2B-orange)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-green)
![MQTT](https://img.shields.io/badge/Protocol-MQTT-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> **IoT system for real-time fire detection and safety monitoring**

---

## 📖 Overview

**IoT Fire Detection & Safety System** is a full-stack solution for monitoring environmental conditions in real time.  
It collects telemetry data from sensors (Smoke, Gas, Temperature), analyzes it for dangerous thresholds, and triggers emergency alerts via a web dashboard.

The system uses **MQTT** for fast and reliable message delivery and a **polling-based REST architecture** for frontend updates.

---

## 🏗 System Architecture

```
[ Sensors ]
     |
     |  MQTT
     v
[ Mosquitto Broker ]
     |
     v
[ Spring Boot Backend ]
     |
     v
[ REST API ]
     |
     v
[ Web Dashboard ]
```

---

## 🚀 Key Features

- 🔥 Automatic Fire Detection
- 📡 Real-time Telemetry Monitoring
- 🚨 CRITICAL Alarm System
- 📊 Live Dashboard with visual alerts
- 💰 Installation Cost Calculator
- 🔐 Authentication & Role-based Security

---

## 🛠 Tech Stack

### Backend
- Java 17
- Spring Boot (Web, Data JPA, Security)
- H2 (Development) / PostgreSQL (Production)
- Gradle

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- REST API (Polling)

### IoT & Infrastructure
- Eclipse Mosquitto (MQTT)
- Python sensor simulation (`paho-mqtt`)

---

## ⚙️ Prerequisites

- JDK 17+
- Eclipse Mosquitto
- Python 3.x

---

## 🏃 Getting Started

### 1️⃣ Install MQTT Broker (Mosquitto)

Install **Eclipse Mosquitto** MQTT Broker for your operating system:

- Windows / macOS / Linux:  
  https://mosquitto.org/download/

After installation, Mosquitto runs automatically as a **system service**
and listens on the default port `1883`.

> Mosquitto is installed system-wide and **does not need to be located in the backend project directory**.

---

### 2️⃣ Run Backend

```bash
./gradlew bootRun
```

---

### 3️⃣ Run Sensor Simulator

```bash
pip install paho-mqtt
python sensor_sim.py
```

---

### 4️⃣ Open Dashboard

Open in browser:  
👉 http://localhost:8081

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/telemetry` | Latest sensor readings |
| GET | `/api/alarms` | List of all alarms |
| GET | `/api/cost` | Installation cost calculator |
| POST | `/api/auth/register` | User registration |
