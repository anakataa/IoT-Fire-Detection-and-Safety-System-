import os, json, time, random, sys
from datetime import datetime, timezone
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# ----- env -----
load_dotenv()
HOST   = os.getenv("BROKER_HOST", "127.0.0.1")
PORT   = int(os.getenv("BROKER_PORT", "1883"))
SITE   = os.getenv("SITE_ID", "lab")
DEVICE = os.getenv("DEVICE_ID", "smoke-001")
QOS    = int(os.getenv("QOS", "1"))

topic_telemetry = f"site/{SITE}/device/{DEVICE}/telemetry"
topic_alarms    = f"site/{SITE}/device/{DEVICE}/alarms"

TEMP_ALARM  = 60.0
SMOKE_ALARM = 300.0
GAS_ALARM   = 500.0

print(f"[BOOT] broker={HOST}:{PORT} device={DEVICE}")
print(f"[BOOT] topics: {topic_telemetry} | {topic_alarms}")

# ----- callbacks for paho-mqtt 2.x -----
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[CONNECT] reason_code={reason_code}")  # 0 == OK

def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"[DISCONNECT] reason_code={reason_code}")

def on_publish(client, userdata, mid, reason_code, properties=None):
    print(f"[PUBLISHED] mid={mid} reason_code={reason_code}")

# ----- client -----
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"{DEVICE}-sim")
client.enable_logger()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

try:
    client.connect(HOST, PORT, keepalive=60)
except Exception as e:
    print(f"[ERROR] connect failed: {e}")
    sys.exit(1)

client.loop_start()

def now_iso(): 
    return datetime.now(timezone.utc).isoformat()

def publish(topic, payload):
    payload_json = json.dumps(payload, ensure_ascii=False)
    print(f"[SEND] {topic} -> {payload_json}")
    r = client.publish(topic, payload_json, qos=QOS, retain=False)
    r.wait_for_publish(timeout=2)

try:
    while True:
        temperature = round(random.uniform(20, 70), 1)
        smoke       = round(random.uniform(0, 400), 1)
        gas         = round(random.uniform(100, 700), 1)

        alarm = (temperature > TEMP_ALARM) or (smoke > SMOKE_ALARM) or (gas > GAS_ALARM)

        telem = {
            "device_id": DEVICE,
            "ts": now_iso(),
            "temperature_c": temperature,
            "smoke_ppm": smoke,
            "gas_ppm": gas,
            "alarm": alarm
        }
        publish(topic_telemetry, telem)

        if alarm:
            if temperature > TEMP_ALARM:
                metric, value, thr = "temperature_c", temperature, TEMP_ALARM
            elif smoke > SMOKE_ALARM:
                metric, value, thr = "smoke_ppm", smoke, SMOKE_ALARM
            else:
                metric, value, thr = "gas_ppm", gas, GAS_ALARM

            publish(topic_alarms, {
                "device_id": DEVICE,
                "ts": now_iso(),
                "type": "ThresholdExceeded",
                "metric": metric,
                "value": value,
                "threshold": thr,
                "severity": "HIGH"
            })

        time.sleep(2)

except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
