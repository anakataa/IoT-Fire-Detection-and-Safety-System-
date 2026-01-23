import paho.mqtt.client as mqtt
import time
import json
import random

# --- ВАЖНО: СЮДА ПИШЕМ IP ТВОЕЙ VM 2 (БРОКЕРА) ---
BROKER = "4.165.87.133" 
PORT = 1883
TOPIC = "sensors/data"
DEVICE_ID = "sens1"
FIRE_MODE = False

print(f"DEBUG: Trying to connect to BROKER: {BROKER} on PORT: {PORT}")

# Обновил аргументы, чтобы работало с новой версией библиотеки без ошибок
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Connected to MQTT Broker! Device: {DEVICE_ID}")
    else:
        print(f"Failed to connect, return code {rc}")

# Используем новую версию API, чтобы не было Warning в логах
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
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
            temperature = round(random.uniform(10.0, 30.0), 1)
            smoke = random.randint(10, 100)
            gas = random.randint(1, 30)

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
