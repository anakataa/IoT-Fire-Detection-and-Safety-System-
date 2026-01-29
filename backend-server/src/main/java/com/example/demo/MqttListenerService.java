package com.example.demo;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.math.BigDecimal;
import java.sql.Timestamp;
import java.time.LocalDateTime;

@Service
public class MqttListenerService {

    @Autowired
    private TelemetryRepository telemetryRepository;

    @Autowired
    private AlarmRepository alarmRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private DeviceRepository deviceRepository;

    private static final double CRITICAL_SMOKE = 350.0;
    private static final double WARNING_SMOKE = 200.0;
    private static final double CRITICAL_TEMP = 60.0;


    private String getOwnerByDeviceId(String deviceId) {
        return deviceRepository.findByDeviceId(deviceId)
                .map(Device::getOwnerUsername)
                .orElse("unknown");
    }

    @Transactional
    public void handleTelemetry(Message<?> message) {
        String payload = (String) message.getPayload();
        Object topicObj = message.getHeaders().get(MqttHeaders.RECEIVED_TOPIC);
        String topic = topicObj != null ? topicObj.toString() : "unknown";

        try {
            SensorDataMessage sensorData = objectMapper.readValue(payload, SensorDataMessage.class);

            Telemetry telemetry = new Telemetry();
            telemetry.setDeviceId(sensorData.getDeviceId());

            String owner = getOwnerByDeviceId(sensorData.getDeviceId());
            telemetry.setUsername(owner);

            LocalDateTime localTime = sensorData.getTimestamp() != null ? sensorData.getTimestamp() : LocalDateTime.now();
            telemetry.setTimestamp(Timestamp.valueOf(localTime));

            telemetry.setTemperature(BigDecimal.valueOf(sensorData.getTemperature()));
            telemetry.setSmokePpm(BigDecimal.valueOf(sensorData.getSmokePpm()));
            telemetry.setGasPpm(BigDecimal.valueOf(sensorData.getGasPpm()));

            telemetry.setAlarm(false);

            telemetryRepository.save(telemetry);

            if (sensorData.getSmokePpm() > CRITICAL_SMOKE) {
                createAndSaveAlarm(sensorData, "CRITICAL", "High Fire Risk", "Smoke", sensorData.getSmokePpm(), CRITICAL_SMOKE);
            } else if (sensorData.getTemperature() > CRITICAL_TEMP) {
                createAndSaveAlarm(sensorData, "CRITICAL", "High Temperature", "Temperature", sensorData.getTemperature(), CRITICAL_TEMP);
            } else if (sensorData.getSmokePpm() > WARNING_SMOKE) {
                createAndSaveAlarm(sensorData, "WARNING", "Elevated Smoke", "Smoke", sensorData.getSmokePpm(), WARNING_SMOKE);
            }

        } catch (IOException e) {
            System.err.println("Error processing MQTT message: " + e.getMessage());
        }
    }

    private void createAndSaveAlarm(SensorDataMessage data, String severity, String type, String metricName, double currentValue, double limitValue) {
        Alarm alarm = new Alarm();
        alarm.setDeviceId(data.getDeviceId());

        String owner = getOwnerByDeviceId(data.getDeviceId());
        alarm.setUsername(owner);

        alarm.setAlarmType(type);
        alarm.setSeverity(severity);

        alarm.setDispatchStatus("SENT");

        LocalDateTime localTime = data.getTimestamp() != null ? data.getTimestamp() : LocalDateTime.now();
        alarm.setTimestamp(Timestamp.valueOf(localTime));

        alarm.setMetric(metricName);
        alarm.setValue(BigDecimal.valueOf(currentValue));
        alarm.setThreshold(BigDecimal.valueOf(limitValue));

        alarmRepository.save(alarm);
        System.out.println("🔥 ALARM CREATED (" + owner + "): " + severity + " (" + metricName + " " + currentValue + ")");
    }
}
