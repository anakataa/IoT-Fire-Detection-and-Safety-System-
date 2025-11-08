# 🔥 IoT Fire Detection and Safety System  

### 📘 Project Overview  
The **Fire Detection and Safety System** is an IoT-based solution designed to enhance safety in homes, offices, and industrial areas.  
The system uses sensors to detect **smoke, gas leaks, or high temperature** and immediately sends **real-time alerts** to users and emergency services via mobile or web application.  

**Goal:** Reduce response time in fire emergencies and minimize damage or casualties.  

---

## ⚙️ System Architecture  

```
[Simulated Device] → [MQTT Broker (Mosquitto)] → [Ingestor Service] → [Azure PostgreSQL]
```

- **Simulator (`sim.py`)** – generates telemetry and alarm data.  
- **MQTT Broker (Mosquitto)** – message hub, local or in Azure Container.  
- **Ingestor (`ingestor.py`)** – subscribes to all topics and writes data into PostgreSQL.  
- **Azure PostgreSQL** – cloud database storing telemetry and alarms.  

---

## 💡 Business Need / Problem Statement  
Traditional fire alarms only provide sound alerts — ineffective if no one is nearby.  
This system ensures **remote visibility, automatic alerts**, and quick reactions.

---

## 🧩 Use Cases  

| Use Case | Description |
|-----------|-------------|
| UC1 – Detect Smoke or Fire | Detect smoke or a sudden rise in temperature. |
| UC2 – Send Real-Time Alerts | Notify users and emergency contacts via network alerts. |
| UC3 – Trigger Local Alarm | Activate a buzzer or siren for nearby warning. |
| UC4 – Monitor Dashboard | Display live telemetry in a dashboard (web/mobile). |
| UC5 – Notify Authorities | Optionally forward alerts to emergency API endpoints. |

---

## 👤 User Stories  
- **As a homeowner**, I want to receive alerts on my phone when fire is detected.  
- **As a manager**, I want to view all building sensors on a dashboard.  
- **As a safety officer**, I want instant alerts for fast response.  
- **As a developer**, I want to analyze telemetry trends for fire risk prediction.  

---

## 🧠 Target Users  
Homeowners, building managers, industrial safety teams, IoT developers.  

---

## 💰 Business Value  
- **Safety:** Early detection protects lives and property.  
- **Automation:** Cloud alerts speed up emergency response.  
- **Scalability:** Easily expandable for larger systems.  
- **Cost Efficiency:** Reduces insurance costs and property loss.  

---

## 🧾 Database Schema (Azure PostgreSQL)  

**Database:** `iot_data` Schema: `iot`  

**Tables:**  
- `iot.telemetry` — device_id, ts, temperature_c, smoke_ppm, gas_ppm, alarm  
- `iot.alarms` — device_id, ts, type, metric, value, threshold, severity  

All records are automatically inserted by the simulator or ingestor.  

---

## 📡 MQTT Topics  

| Topic | Description |
|--------|-------------|
| `site/<site_id>/device/<device_id>/telemetry` | Regular telemetry data |
| `site/<site_id>/device/<device_id>/alarms` | Alarm events (ThresholdExceeded) |

**Example message:**  
```json
{
  "device_id": "smoke-001",
  "ts": "2025-11-08T13:25:30Z",
  "temperature_c": 62.3,
  "smoke_ppm": 280.5,
  "gas_ppm": 580.1,
  "alarm": true
}
```

---

## 🧱 Prerequisites  
Install:  
- Docker Desktop  
- Python 3.11+  
- Git  

---

## 🚀 How to Run the Project  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/anakataa/IoT-Fire-Detection-and-Safety-System-.git
cd IoT-Fire-Detection-and-Safety-System-
```

### 2️⃣ Start MQTT Broker  
```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto:2
```

Check it:  
```bash
docker ps
```

---

### 3️⃣ Configure Environment  
Create a `.env` file:  
```ini
BROKER_HOST=127.0.0.1
BROKER_PORT=1883
SITE_ID=lab
DEVICE_ID=smoke-001
QOS=1

PGHOST=iotdemo-pg.postgres.database.azure.com
PGPORT=5432
PGDATABASE=iot_data
PGUSER=iotadmin
PGPASSWORD=FireDemo_2024
PGSSLMODE=require
```

---

### 4️⃣ Launch Services  

#### a) Ingestor (writes to DB)
```bash
python ingestor.py
```

#### b) Simulator (sends telemetry)
```bash
python sim.py
```

---

### 5️⃣ Verify Data in Database  
```sql
SELECT * FROM iot.telemetry ORDER BY id DESC LIMIT 5;
SELECT * FROM iot.alarms ORDER BY id DESC LIMIT 5;
```

---

### ✅ Task Summary  

| Task | Description | Status |
|------|--------------|--------|
| #3 – MQTT Broker Service | Launch broker, define topics, verify communication | ✅ Done |
| #4 – Device / Simulator | Create virtual sensor, send telemetry & alarms | ✅ Done |
| #5 – Data Storage | Build schema in Azure PostgreSQL and store data | ✅ Done |

---

## 🧰 Tools & Technologies  
- Python 3.11  
- Paho MQTT 2.x  
- psycopg 3  
- Docker / Mosquitto  
- Azure PostgreSQL  
- dotenv  

---

## 🧾 Project Structure  
```
IoT-Fire-Detection-and-Safety-System-
│
├── iot-sim/
│   ├── sim.py          # sensor simulator
│   ├── ingestor.py     # MQTT listener → PostgreSQL
│   ├── .env            # configuration
│   └── requirements.txt
└── README.md
```

---

## 👨‍💻 Author  
**dburan** – IoT & Cloud Computing Project (CDV  Dmytro Buran 29911)  
📧 dburan@edu.cdv.pl  

---

💬 *All components – MQTT, Simulator, Ingestor, and Azure Database – are connected and verified.*  
🚀 *Fully working IoT Fire Detection System ready for presentation and deployment.*
