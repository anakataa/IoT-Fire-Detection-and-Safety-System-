package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AppUserRepository userRepository;

    @Autowired
    private DeviceRepository deviceRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @GetMapping("/check")
    public String checkAuth() {
        return "OK";
    }

    @PostMapping("/register")
    public String registerUser(@RequestParam String username, @RequestParam String password) {
        if (userRepository.findByUsername(username).isPresent()) {
            return "Error: User already exists!";
        }

        AppUser user = new AppUser();
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(password)); // ШИФРУЕМ ПАРОЛЬ!
        user.setRole("USER");
        userRepository.save(user);

        return "User registered successfully!";
    }


    @PostMapping("/add-device")
    public String addDevice(@RequestParam String deviceId, @RequestParam String username) {

        if (deviceRepository.existsById(deviceId)) {
            return deviceRepository.findById(deviceId)
                    .map(device -> {
                        if (device.getOwnerUsername().equals(username)) {
                            return "Info: You already own this device.";
                        } else {
                            return "Error: Device '" + deviceId + "' is already taken by another user!";
                        }
                    })
                    .orElse("Error: Unknown error");
        }

        Device device = new Device();
        device.setDeviceId(deviceId);
        device.setOwnerUsername(username);
        deviceRepository.save(device);

        return "Success: Device " + deviceId + " linked to " + username;
    }
}