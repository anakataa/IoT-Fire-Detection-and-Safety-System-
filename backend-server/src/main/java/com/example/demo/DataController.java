package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

/**
 * Main REST controller providing HTTP endpoints for the frontend.
 *
 * @CrossOrigin(origins = "*") allows requests from external domains (e.g., React frontend),
 * preventing CORS errors.
 */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class DataController {

    // Repository connections
    @Autowired
    private TelemetryRepository telemetryRepository;

    @Autowired
    private AlarmRepository alarmRepository;

    /**
     * Endpoint #1: Get latest telemetry records
     * URL: /api/telemetry
     * @return last 20 telemetry entries
     */
    @GetMapping("/telemetry")
    public List<Telemetry> getLatestTelemetry() {
        return telemetryRepository.findTop20ByOrderByTimestampDesc();
    }

    /**
     * Endpoint #2: Get latest alarms (default: critical)
     * URL: /api/alarms
     * @return list of alarms
     *
     * Note: This still uses filtering by "critical" until the repository method
     * for "find last 20 of any severity" is added.
     */
    @GetMapping("/alarms")
    public List<Alarm> getAllAlarms() {
        return alarmRepository.findBySeverityOrderByTimestampDesc("critical");
    }

    /**
     * Endpoint #3: Get alarms by severity
     * URLs example:
     *   /api/alarms/critical
     *   /api/alarms/warning
     *
     * @param severity severity extracted from the URL
     * @return list of alarms with the given severity
     */
    @GetMapping("/alarms/{severity}")
    public List<Alarm> getAlarmsBySeverity(@PathVariable String severity) {
        return alarmRepository.findBySeverityOrderByTimestampDesc(severity);
    }

    /**
     * Endpoint #4: Cost calculator
     * URL example: /api/cost?sensors=10&rooms=4
     *
     * @param sensors number of sensors
     * @param rooms number of rooms
     * @return JSON with calculated costs
     */
    @GetMapping("/cost")
    public Map<String, BigDecimal> getCost(
            @RequestParam int sensors,
            @RequestParam int rooms
    ) {
        // Pricing constants
        BigDecimal sensorPrice = new BigDecimal("50.00");
        BigDecimal roomInstallPrice = new BigDecimal("150.00");
        BigDecimal monthlyFee = new BigDecimal("20.00");

        // Calculations
        BigDecimal equipmentCost = sensorPrice.multiply(new BigDecimal(sensors));
        BigDecimal installCost = roomInstallPrice.multiply(new BigDecimal(rooms));
        BigDecimal totalOneTimeCost = equipmentCost.add(installCost);
        BigDecimal totalMonthlyCost = monthlyFee;

        // JSON response
        return Map.of(
                "equipmentCost", equipmentCost,
                "installCost", installCost,
                "totalOneTimeCost", totalOneTimeCost,
                "totalMonthlyCost", totalMonthlyCost
        );
    }
}
