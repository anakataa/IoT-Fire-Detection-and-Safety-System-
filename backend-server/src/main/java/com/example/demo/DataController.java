package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.security.Principal;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class DataController {

    @Autowired
    private TelemetryRepository telemetryRepository;

    @Autowired
    private AlarmRepository alarmRepository;

    @GetMapping("/telemetry")
    public List<Telemetry> getLatestTelemetry(Principal principal) {
        if (principal == null) return List.of();
        return telemetryRepository.findTop20ByUsernameOrderByTimestampDesc(principal.getName());
    }

    @GetMapping("/alarms")
    public List<Alarm> getAllAlarms(Principal principal) {
        if (principal == null) return List.of();
        return alarmRepository.findAllByUsernameOrderByTimestampDesc(principal.getName());
    }

    @GetMapping("/alarms/{severity}")
    public List<Alarm> getAlarmsBySeverity(@PathVariable String severity, Principal principal) {
        if (principal == null) return List.of();
        return alarmRepository.findByUsernameAndSeverityOrderByTimestampDesc(
                principal.getName(),
                severity.toUpperCase()
        );
    }

    @PostMapping("/alarms/{id}/confirm")
    public ResponseEntity<String> confirmDispatch(@PathVariable Long id, Principal principal) {
        Optional<Alarm> alarmOpt = alarmRepository.findById(id);
        if (alarmOpt.isEmpty()) return ResponseEntity.notFound().build();

        Alarm alarm = alarmOpt.get();
        if (!alarm.getUsername().equals(principal.getName()))
            return ResponseEntity.status(403).body("Not yours");

        alarm.setDispatchStatus("SENT");
        alarmRepository.save(alarm);

        return ResponseEntity.ok("Confirmed");
    }

    @PostMapping("/alarms/{id}/cancel")
    public ResponseEntity<String> cancelDispatch(@PathVariable Long id, Principal principal) {
        Optional<Alarm> alarmOpt = alarmRepository.findById(id);
        if (alarmOpt.isEmpty()) return ResponseEntity.notFound().build();

        Alarm alarm = alarmOpt.get();
        if (!alarm.getUsername().equals(principal.getName()))
            return ResponseEntity.status(403).body("Not yours");

        alarm.setDispatchStatus("CANCELLED");
        alarmRepository.save(alarm);

        return ResponseEntity.ok("Cancelled");
    }

    @DeleteMapping("/alarms/{id}")
    public ResponseEntity<String> deleteAlarm(@PathVariable Long id, Principal principal) {
        Optional<Alarm> alarmOpt = alarmRepository.findById(id);
        if (alarmOpt.isEmpty()) return ResponseEntity.notFound().build();
        if (!alarmOpt.get().getUsername().equals(principal.getName()))
            return ResponseEntity.status(403).build();

        alarmRepository.deleteById(id);
        return ResponseEntity.ok("Deleted");
    }

    @GetMapping("/cost")
    public Map<String, BigDecimal> getCost(@RequestParam int sensors, @RequestParam int rooms) {
        BigDecimal sensorPrice = new BigDecimal("50.00");
        BigDecimal roomInstallPrice = new BigDecimal("150.00");
        BigDecimal monthlyFee = new BigDecimal("20.00");

        BigDecimal equipmentCost = sensorPrice.multiply(new BigDecimal(sensors));
        BigDecimal installCost = roomInstallPrice.multiply(new BigDecimal(rooms));
        BigDecimal totalOneTimeCost = equipmentCost.add(installCost);

        return Map.of(
                "equipmentCost", equipmentCost,
                "installCost", installCost,
                "totalOneTimeCost", totalOneTimeCost,
                "totalMonthlyCost", monthlyFee
        );
    }
}
