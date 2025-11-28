FROM eclipse-mosquitto:latest

# Открываем порты для Mosquitto (1883 — для MQTT, 9001 — для WebSockets)
EXPOSE 1883
EXPOSE 9001


COPY config/mosquitto.conf /etc/mosquitto/mosquitto.conf


# Запуск Mosquitto
CMD ["mosquitto", "-c", "/etc/mosquitto/mosquitto.conf"]
