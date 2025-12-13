package com.example.demo;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "devices")
@Data
public class Device {

    @Id
    private String deviceId;

    private String ownerUsername;
}