# IoT-Fire-Detection-and-Safety-System-
project by IOT 

# Fire Detection and Safety System – Business Context

## 1. Project Overview
The **Fire Detection and Safety System** is an IoT-based solution designed to enhance safety in homes, offices, and industrial areas.  
The system uses sensors to detect **smoke, gas leaks, or high temperature** and immediately sends **real-time alerts** to users and emergency services via mobile or web application.  

**Goal:** Reduce response time in fire emergencies and minimize damage or casualties.

---

## 2. Business Need / Problem Statement
Fire incidents cause major property damage, injuries, and loss of life every year. Traditional fire alarms only provide sound alerts, which are ineffective if no one is nearby.  

There is a need for a **connected, intelligent fire alert system** that notifies users remotely and automatically triggers safety measures.

---

## 3. Use Cases

| Use Case | Description |
|----------|-------------|
| UC1 – Detect Smoke or Fire | Detect smoke or a sudden rise in temperature through sensors. |
| UC2 – Send Real-Time Alerts | Send instant alerts to users’ smartphones and emergency contacts when fire or gas leak is detected. |
| UC3 – Trigger Alarm | Activate a local buzzer or siren to alert nearby individuals. |
| UC4 – Monitor via Dashboard | Monitor sensor data (smoke level, temperature, gas) via a web/mobile dashboard. |
| UC5 – Notify Fire Department | Optionally send data to the local fire department or emergency API. |

---

## 4. User Stories
- **As a homeowner**, I want to get a mobile alert when smoke or fire is detected so I can act immediately.  
- **As a building manager**, I want a dashboard showing real-time data from all fire sensors in the building.  
- **As a safety officer**, I want to receive automatic alerts to dispatch help faster.  
- **As a developer**, I want to collect and visualize sensor data to analyze fire risks and trends.

---

## 5. Target Users
- Homeowners  
- Office and building managers  
- Industrial safety teams  
- IoT developers or researchers

---

## 6. Business Value
- **Safety:** Early detection reduces risk to life and property.  
- **Automation:** Real-time alerts and data monitoring improve emergency response.  
- **Scalability:** Can be expanded for smart buildings or industrial systems.  
- **Cost-Effective:** Reduces insurance costs and property loss.

---

# 🚀 How to Run the Project

This section explains how to launch the complete IoT Fire Detection and Safety System on your local machine.

---

## 🧱 Prerequisites
Before running, make sure you have installed:
- **Docker Desktop**
- **Python 3.10+**
- **Git**

---

## ⚙️ 1. Clone the Repository
```bash
git clone https://github.com/anakataa/IoT-Fire-Detection-and-Safety-System-.git
cd IoT-Fire-Detection-and-Safety-System-
```

---

## 🐳 2. Start MQTT Broker (Mosquitto)
Run the broker in a Docker container:
```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto:2
```

Verify that it’s running:
```bash
docker ps
```
You should see a container named **mosquitto** with port **1883** open.

---

## 💡 3. Run the IoT Simulator

Navigate to the simulator folder:
```bash
cd iot-sim
```

Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:
```bash
pip install paho-mqtt python-dotenv
```

Run the simulator:
```bash
python sim.py
```

✅ This will start sending random **temperature, smoke, and gas** data to the MQTT broker.

---

## 🔍 4. Monitor MQTT Messages

Open a new PowerShell window and subscribe to all topics:
```bash
mosquitto_sub -h localhost -t "site/+/device/+/telemetry" -v
```

You should see messages like:
```
site/lab/device/smoke-001/telemetry {"temperature_c":25.6,"smoke_ppm":120.3,"gas_ppm":220.1,"alarm":false}
```

---

## 🚨 5. View Alarm Messages
When thresholds are exceeded, alarms are published here:
```bash
mosquitto_sub -h localhost -t "site/+/device/+/alarms" -v
```

Example output:
```
site/lab/device/smoke-001/alarms {"type":"ThresholdExceeded","metric":"gas_ppm","value":598.9,"severity":"HIGH"}
```

---

## 🧩 6. Project Structure
```
IoT-Fire-Detection-and-Safety-System-
│
├── mqtt-broker/        # Mosquitto broker config
├── iot-sim/            # IoT sensor simulator in Python
├── README.md           # Project documentation (this file)
└── .gitignore          # Excludes venv, .env, and cache files
```

---

## ✅ Summary
By following these steps:
1. The MQTT broker runs locally inside Docker.  
2. The Python simulator publishes telemetry and alarm data.  
3. Messages can be viewed in real time through `mosquitto_sub`.

This demonstrates a complete **IoT Fire Detection System** pipeline — from data generation to message transmission and alerting.

---

*Developed for educational purposes as part of the IoT & Cloud Computing course.*
