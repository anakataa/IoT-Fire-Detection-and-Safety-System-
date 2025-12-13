package com.example.demo;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class SensorDataMessage {
    private String deviceId;
    private double temperature;
    private double smokePpm;
    private double gasPpm;

    private boolean alarm;

    private LocalDateTime timestamp;
}