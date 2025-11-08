import os, json, time, random, sys
from datetime import datetime, timezone

from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# ======== PostgreSQL (psycopg 3) ========
try:
    import psycopg
except ImportError:
    psycopg = None

# ======== ENV ========
load_dotenv()

# MQTT
HOST   = os.getenv("BROKER_HOST", "127.0.0.1")
PORT   = int(os.getenv("BROKER_PORT", "1883"))
SITE   = os.getenv("SITE_ID", "lab")
DEVICE = os.getenv("DEVICE_ID", "smoke-001")
QOS    = int(os.getenv("QOS", "1"))

topic_telemetry = f"site/{SITE}/device/{DEVICE}/telemetry"
topic_alarms    = f"site/{SITE}/device/{DEVICE}/alarms"

# thresholds
TEMP_ALARM  = float(os.getenv("TEMP_ALARM", 60.0))
SMOKE_ALARM = float(os.getenv("SMOKE_ALARM", 300.0))
GAS_ALARM   = float(os.getenv("GAS_ALARM", 500.0))

# PostgreSQL
PGHOST     = os.getenv("PGHOST")
PGPORT     = int(os.getenv("PGPORT", "5432"))
PGDATABASE = os.getenv("PGDATABASE", "iot_data")
PGUSER     = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGSSLMODE  = os.getenv("PGSSLMODE", "require")

PG_ENABLED = all([psycopg is not None, PGHOST, PGUSER, PGPASSWORD])

print(f"[BOOT] broker={HOST}:{PORT} device={DEVICE}")
print(f"[BOOT] topics: {topic_telemetry} | {topic_alarms}")
print(f"[BOOT] postgres: {'ENABLED' if PG_ENABLED else 'DISABLED'}")

# ======== PostgreSQL helpers ========
_pg_conn = None
_pg_cur  = None

def pg_connect():
    """Lazy connect + cursor create."""
    global _pg_conn, _pg_cur
    if not PG_ENABLED:
        return
    if _pg_conn is not None and not _pg_conn.closed:
        return
    try:
        _pg_conn = psycopg.connect(
            host=PGHOST,
            port=PGPORT,
            dbname=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD,
            sslmode=PGSSLMODE,
            connect_timeout=10,
        )
        _pg_conn.autocommit = True
        _pg_cur = _pg_conn.cursor()
        print("[PG] connected")
        pg_init_schema()
    except Exception as e:
        print(f"[PG][ERROR] connect failed: {e}")
        _pg_conn = None
        _pg_cur  = None

def pg_safe_close():
    global _pg_conn, _pg_cur
    try:
        if _pg_cur:  _pg_cur.close()
    except: ...
    try:
        if _pg_conn: _pg_conn.close()
    except: ...
    _pg_cur  = None
    _pg_conn = None

def pg_init_schema():
    """Create schema/tables/indexes if not exist."""
    if _pg_cur is None:
        return
    ddl = """
    CREATE SCHEMA IF NOT EXISTS iot;

    CREATE TABLE IF NOT EXISTS iot.telemetry (
        id            BIGSERIAL PRIMARY KEY,
        device_id     TEXT        NOT NULL,
        ts            TIMESTAMPTZ NOT NULL DEFAULT now(),
        temperature_c NUMERIC(6,2),
        smoke_ppm     NUMERIC(10,2),
        gas_ppm       NUMERIC(10,2),
        alarm         BOOLEAN NOT NULL DEFAULT false
    );
    CREATE INDEX IF NOT EXISTS idx_telemetry_device_ts
        ON iot.telemetry (device_id, ts DESC);

    CREATE TABLE IF NOT EXISTS iot.alarms (
        id         BIGSERIAL PRIMARY KEY,
        device_id  TEXT        NOT NULL,
        ts         TIMESTAMPTZ NOT NULL DEFAULT now(),
        type       TEXT        NOT NULL,
        metric     TEXT        NOT NULL,
        value      NUMERIC(10,2) NOT NULL,
        threshold  NUMERIC(10,2) NOT NULL,
        severity   TEXT        NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_alarms_device_ts
        ON iot.alarms (device_id, ts DESC);
    """
    _pg_cur.execute(ddl)

def pg_insert_telemetry(payload: dict):
    """Insert into iot.telemetry."""
    if not PG_ENABLED:
        return
    try:
        pg_connect()
        if _pg_cur is None:
            return
        _pg_cur.execute(
            """
            INSERT INTO iot.telemetry(device_id, ts, temperature_c, smoke_ppm, gas_ppm, alarm)
            VALUES (%(device_id)s, %(ts)s, %(temperature_c)s, %(smoke_ppm)s, %(gas_ppm)s, %(alarm)s)
            """,
            payload
        )
    except Exception as e:
        print(f"[PG][ERROR] insert telemetry: {e}")
        pg_safe_close()  # reconnect next time

def pg_insert_alarm(payload: dict):
    """Insert into iot.alarms."""
    if not PG_ENABLED:
        return
    try:
        pg_connect()
        if _pg_cur is None:
            return
        _pg_cur.execute(
            """
            INSERT INTO iot.alarms(device_id, ts, type, metric, value, threshold, severity)
            VALUES (%(device_id)s, %(ts)s, %(type)s, %(metric)s, %(value)s, %(threshold)s, %(severity)s)
            """,
            payload
        )
    except Exception as e:
        print(f"[PG][ERROR] insert alarm: {e}")
        pg_safe_close()

# ======== MQTT callbacks (paho-mqtt 2.x) ========
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[CONNECT] reason_code={reason_code}")

def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"[DISCONNECT] reason_code={reason_code}")

def on_publish(client, userdata, mid, reason_code, properties=None):
    print(f"[PUBLISHED] mid={mid} reason_code={reason_code}")

# ======== MQTT client ========
# ВАЖНО: первый аргумент — CallbackAPIVersion (для v2 сигнатур)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"{DEVICE}-sim")
client.enable_logger()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

try:
    client.connect(HOST, PORT, keepalive=60)
except Exception as e:
    print(f"[ERROR] MQTT connect failed: {e}")
    sys.exit(1)

client.loop_start()

# ======== utils ========
def now_iso():
    return datetime.now(timezone.utc).isoformat()

def mqtt_publish(topic, payload):
    data = json.dumps(payload, ensure_ascii=False)
    print(f"[SEND] {topic} -> {data}")
    try:
        r = client.publish(topic, data, qos=QOS, retain=False)
        r.wait_for_publish(timeout=2)
    except Exception as e:
        print(f"[MQTT][ERROR] publish: {e}")

# ======== main loop ========
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

        # 1) MQTT
        mqtt_publish(topic_telemetry, telem)
        # 2) PostgreSQL
        pg_insert_telemetry(telem)

        if alarm:
            if temperature > TEMP_ALARM:
                metric, value, thr = "temperature_c", temperature, TEMP_ALARM
            elif smoke > SMOKE_ALARM:
                metric, value, thr = "smoke_ppm", smoke, SMOKE_ALARM
            else:
                metric, value, thr = "gas_ppm", gas, GAS_ALARM

            alarm_payload = {
                "device_id": DEVICE,
                "ts": now_iso(),
                "type": "ThresholdExceeded",
                "metric": metric,
                "value": value,
                "threshold": thr,
                "severity": "HIGH"
            }

            mqtt_publish(topic_alarms, alarm_payload)
            pg_insert_alarm(alarm_payload)

        time.sleep(2)

except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    pg_safe_close()
