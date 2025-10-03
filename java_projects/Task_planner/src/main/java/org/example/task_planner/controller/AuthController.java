package org.example.task_planner.controller;

import org.example.task_planner.dto.LoginDTO;
import org.example.task_planner.dto.UserDTO;
import org.example.task_planner.dto.UserLoginResponseDTO;
import org.example.task_planner.model.User;
import org.example.task_planner.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody UserDTO userDTO) {
        // Check if email already exists
        if (userService.emailExists(userDTO.getEmail())) {
            return ResponseEntity.badRequest().body("Email already registered");
        }

        // Check if user ID already exists
        if (userService.userIdExists(userDTO.getUserId())) {
            return ResponseEntity.badRequest().body("User ID already in use");
        }

        // Create new user
        User user = new User();
        user.setName(userDTO.getName());
        user.setSurname(userDTO.getSurname());
        user.setUserId(userDTO.getUserId());
        user.setEmail(userDTO.getEmail());
        user.setPassword(userDTO.getPassword()); // Automatically encrypted

        User savedUser = userService.registerUser(user);

        Map<String, Object> response = new HashMap<>();
        response.put("message", "User registered successfully");
        response.put("userId", savedUser.getId());

        return ResponseEntity.ok(response);
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginDTO loginDTO) {
        Optional<User> user = userService.login(loginDTO.getEmail(), loginDTO.getPassword());

        if (user.isPresent()) {
            // Convert User to UserResponseDTO (without password)
            UserLoginResponseDTO userResponse = new UserLoginResponseDTO();
            userResponse.setId(user.get().getId());
            userResponse.setName(user.get().getName());
            userResponse.setSurname(user.get().getSurname());
            userResponse.setUserId(user.get().getUserId());
            userResponse.setEmail(user.get().getEmail());

            Map<String, Object> response = new HashMap<>();
            response.put("message", "Login successful");
            response.put("user", userResponse); // Now without password

            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body("Invalid email or password");
        }
    }
}