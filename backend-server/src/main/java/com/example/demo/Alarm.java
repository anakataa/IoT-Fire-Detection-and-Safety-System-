package com.example.demo;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.sql.Timestamp;

@Entity
@Table(name = "alarms", schema = "iot")
@Data
public class Alarm {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;


    @Column(name = "device_id", nullable = false)
    private String deviceId;

    @Column(name = "username")
    private String username;

    @Column(name = "ts", nullable = false)
    private Timestamp timestamp;


    @Column(name = "dispatch_status")
    private String dispatchStatus = "PENDING";

    @Column(name = "is_active", nullable = false)
    private boolean active = true;

    @Column(name = "is_acknowledged", nullable = false)
    private boolean acknowledged = false;


    @Column(name = "severity")
    private String severity;

    @Column(name = "metric")
    private String metric;

    @Column(name = "type")
    private String alarmType;

    @Column(precision = 10, scale = 2)
    private BigDecimal value;

    @Column(precision = 10, scale = 2)
    private BigDecimal threshold;
}