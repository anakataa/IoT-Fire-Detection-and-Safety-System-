-- Создаём схему iot, если её нет
CREATE SCHEMA IF NOT EXISTS iot;

-- Таблица телеметрии
CREATE TABLE IF NOT EXISTS iot.telemetry (
    id            BIGSERIAL PRIMARY KEY,
    device_id     TEXT        NOT NULL,
    ts            TIMESTAMPTZ NOT NULL DEFAULT now(),
    temperature_c NUMERIC(6,2),
    smoke_ppm     NUMERIC(10,2),
    gas_ppm       NUMERIC(10,2),
    alarm         BOOLEAN     NOT NULL DEFAULT false
);

-- Таблица тревог
CREATE TABLE IF NOT EXISTS iot.alarms (
    id        BIGSERIAL PRIMARY KEY,
    device_id TEXT        NOT NULL,
    ts        TIMESTAMPTZ NOT NULL DEFAULT now(),
    type      TEXT        NOT NULL,
    metric    TEXT        NOT NULL,
    value     NUMERIC(10,2) NOT NULL,
    threshold NUMERIC(10,2) NOT NULL,
    severity  TEXT        NOT NULL
);

-- Права пользователю iot
GRANT ALL ON SCHEMA iot TO iot;
GRANT ALL ON ALL TABLES IN SCHEMA iot TO iot;

-- Чтобы можно было писать просто SELECT * FROM telemetry;
ALTER ROLE iot SET search_path TO iot, public;
