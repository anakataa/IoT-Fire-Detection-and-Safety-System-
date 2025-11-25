package com.example.demo;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.sql.Timestamp;

@Entity
@Table(name = "telemetry", schema = "iot")
public class Telemetry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "device_id")
    private String deviceId;

    @Column(name = "ts")
    private Timestamp timestamp;

    // Using BigDecimal for precise numeric sensor values
    @Column(name = "temperature_c")
    private BigDecimal temperature;

    @Column(name = "smoke_ppm")
    private BigDecimal smokePpm;

    @Column(name = "gas_ppm")
    private BigDecimal gasPpm;

    private Boolean alarm;

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public void setDeviceId(String deviceId) {
        this.deviceId = deviceId;
    }

    public Timestamp getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Timestamp timestamp) {
        this.timestamp = timestamp;
    }

    public BigDecimal getTemperature() {
        return temperature;
    }

    public void setTemperature(BigDecimal temperature) {
        this.temperature = temperature;
    }

    public BigDecimal getSmokePpm() {
        return smokePpm;
    }

    public void setSmokePpm(BigDecimal smokePpm) {
        this.smokePpm = smokePpm;
    }

    public BigDecimal getGasPpm() {
        return gasPpm;
    }

    public void setGasPpm(BigDecimal gasPpm) {
        this.gasPpm = gasPpm;
    }

    public Boolean getAlarm() {
        return alarm;
    }

    public void setAlarm(Boolean alarm) {
        this.alarm = alarm;
    }
}
