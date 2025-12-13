package com.example.demo;

import jakarta.persistence.*;
import lombok.Data;

import java.math.BigDecimal;
import java.sql.Timestamp;

@Entity
@Table(name = "telemetry", schema = "iot")
@Data
public class Telemetry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "device_id")
    private String deviceId;

    @Column(name = "ts")
    private Timestamp timestamp;

    @Column(name = "temperature_c")
    private BigDecimal temperature;

    @Column(name = "smoke_ppm")
    private BigDecimal smokePpm;

    @Column(name = "gas_ppm")
    private BigDecimal gasPpm;

    private Boolean alarm;

    private String username;



}
