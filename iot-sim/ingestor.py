import os, json, time, traceback
from datetime import datetime, timezone
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# DB
import psycopg

load_dotenv()

# --- MQTT ---
BROKER_HOST = os.getenv("BROKER_HOST", "127.0.0.1")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
QOS         = int(os.getenv("QOS", "1"))

# Слушаем все девайсы во всех сайтах:
TOPIC_TELEMETRY = "site/+/device/+/telemetry"
TOPIC_ALARMS    = "site/+/device/+/alarms"

# --- PostgreSQL ---
PGHOST     = os.getenv("PGHOST")
PGPORT     = int(os.getenv("PGPORT", "5432"))
PGDATABASE = os.getenv("PGDATABASE", "iot_data")
PGUSER     = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGSSLMODE  = os.getenv("PGSSLMODE", "require")

# --- DB helpers ---
_conn = None
_cur  = None

def pg_connect():
    global _conn, _cur
    if _conn and not _conn.closed:
        return
    _conn = psycopg.connect(
        host=PGHOST, port=PGPORT, dbname=PGDATABASE,
        user=PGUSER, password=PGPASSWORD, sslmode=PGSSLMODE,
        connect_timeout=10,
    )
    _conn.autocommit = True
    _cur = _conn.cursor()
    print("[PG] connected")

def pg_init_schema():
    pg_connect()
    _cur.execute("""
        CREATE SCHEMA IF NOT EXISTS iot;

        CREATE TABLE IF NOT EXISTS iot.telemetry (
            id BIGSERIAL PRIMARY KEY,
            device_id     TEXT NOT NULL,
            ts            TIMESTAMPTZ NOT NULL DEFAULT now(),
            temperature_c NUMERIC(6,2),
            smoke_ppm     NUMERIC(10,2),
            gas_ppm       NUMERIC(10,2),
            alarm         BOOLEAN NOT NULL DEFAULT false
        );
        CREATE INDEX IF NOT EXISTS idx_telemetry_device_ts
            ON iot.telemetry (device_id, ts DESC);

        CREATE TABLE IF NOT EXISTS iot.alarms (
            id BIGSERIAL PRIMARY KEY,
            device_id TEXT NOT NULL,
            ts        TIMESTAMPTZ NOT NULL DEFAULT now(),
            type      TEXT NOT NULL,      -- 'ThresholdExceeded'
            metric    TEXT NOT NULL,      -- temperature_c | smoke_ppm | gas_ppm
            value     NUMERIC(10,2) NOT NULL,
            threshold NUMERIC(10,2) NOT NULL,
            severity  TEXT NOT NULL       -- HIGH/...
        );
        CREATE INDEX IF NOT EXISTS idx_alarms_device_ts
            ON iot.alarms (device_id, ts DESC);
    """)
    print("[PG] schema ready")

def pg_insert_telemetry(p: dict):
    pg_connect()
    _cur.execute("""
        INSERT INTO iot.telemetry(device_id, ts, temperature_c, smoke_ppm, gas_ppm, alarm)
        VALUES (%(device_id)s, %(ts)s, %(temperature_c)s, %(smoke_ppm)s, %(gas_ppm)s, %(alarm)s)
    """, p)

def pg_insert_alarm(p: dict):
    pg_connect()
    _cur.execute("""
        INSERT INTO iot.alarms(device_id, ts, type, metric, value, threshold, severity)
        VALUES (%(device_id)s, %(ts)s, %(type)s, %(metric)s, %(value)s, %(threshold)s, %(severity)s)
    """, p)

# --- MQTT callbacks (paho-mqtt 2.x) ---
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[MQTT] connect rc={reason_code}")
    # подписываемся после коннекта (или реконнекта)
    client.subscribe(TOPIC_TELEMETRY, qos=QOS)
    client.subscribe(TOPIC_ALARMS, qos=QOS)
    print(f"[MQTT] subscribed: {TOPIC_TELEMETRY} & {TOPIC_ALARMS}")

def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"[MQTT] disconnect rc={reason_code}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except Exception as e:
        print(f"[WARN] bad json on {msg.topic}: {e}")
        return

    # topic: site/<site>/device/<device>/telemetry|alarms
    parts = msg.topic.split("/")
    if len(parts) < 5:
        print(f"[WARN] unexpected topic: {msg.topic}")
        return
    device_id = parts[3]  # site/<site>/device/<THIS>/...

    # У всех сообщений нормализуем timestamp
    ts = payload.get("ts")
    if not ts:
        ts = datetime.now(timezone.utc).isoformat()

    if parts[-1] == "telemetry":
        row = {
            "device_id": device_id,
            "ts": ts,
            "temperature_c": payload.get("temperature_c"),
            "smoke_ppm":     payload.get("smoke_ppm"),
            "gas_ppm":       payload.get("gas_ppm"),
            "alarm":         bool(payload.get("alarm", False)),
        }
        try:
            pg_insert_telemetry(row)
            print(f"[DB] telem ↑ {device_id} {row['ts']}")
        except Exception:
            print("[ERR] telem insert failed")
            traceback.print_exc()

    elif parts[-1] == "alarms":
        # ожидаем формат sim.py
        row = {
            "device_id": device_id,
            "ts":        ts,
            "type":      payload.get("type", "ThresholdExceeded"),
            "metric":    payload.get("metric"),
            "value":     payload.get("value"),
            "threshold": payload.get("threshold"),
            "severity":  payload.get("severity", "HIGH"),
        }
        try:
            pg_insert_alarm(row)
            print(f"[DB] alarm ↑ {device_id} {row['metric']}={row['value']}")
        except Exception:
            print("[ERR] alarm insert failed")
            traceback.print_exc()

def main():
    # DB init
    pg_init_schema()

    # MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ingestor-01")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # автопереподключение
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    print(f"[BOOT] mqtt={BROKER_HOST}:{BROKER_PORT}  qos={QOS}")
    print(f"[BOOT] pg={PGHOST}:{PGPORT}/{PGDATABASE} user={PGUSER}")

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()  # бесконечный цикл с авто-реконнектом

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("bye")
