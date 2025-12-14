import paho.mqtt.client as mqtt
import time
import json
import random

BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/data"
DEVICE_ID = "Alexpidr_sensor"
FIRE_MODE = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker! Device: {DEVICE_ID}")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client()
client.on_connect = on_connect

try:
    client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"Connection error: {e}")
    exit()

client.loop_start()

print("Simulation started. Press Ctrl+C to stop.")
print(f"FIRE MODE is: {'ON' if FIRE_MODE else 'OFF'}")

try:
    while True:
        if FIRE_MODE:
            temperature = round(random.uniform(50.0, 90.0), 1)
            smoke = random.randint(400, 800)
            gas = random.randint(100, 300)
        else:
            temperature = round(random.uniform(20.0, 25.0), 1)
            smoke = random.randint(10, 400)
            gas = random.randint(0, 10)

        payload = {
            "deviceId": DEVICE_ID,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "temperature": temperature,
            "smokePpm": smoke,
            "gasPpm": gas
        }

        payload_json = json.dumps(payload)
        client.publish(TOPIC, payload_json)
        print(f"Sent: {payload_json}")
        time.sleep(3)

except KeyboardInterrupt:
    print("Simulation stopped.")
    client.loop_stop()
    client.disconnect()
