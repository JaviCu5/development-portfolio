package org.example.task_planner.controller;

import org.example.task_planner.dto.LoginDTO;
import org.example.task_planner.dto.UserDTO;
import org.example.task_planner.model.User;
import org.example.task_planner.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
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
        // Verification of existing email
        if (userService.emailExists(userDTO.getEmail())) {
            return ResponseEntity.badRequest().body("The email is registered");
        }

        // Verification of existing userId
        if (userService.userIdExists(userDTO.getUserId())) {
            return ResponseEntity.badRequest().body("The user ID is already used");
        }

        // Creation of a new User
        User user = new User();
        user.setName(userDTO.getName());
        user.setSurname(userDTO.getSurname());
        user.setUserId(userDTO.getUserId());
        user.setEmail(userDTO.getEmail());
        user.setPassword(userDTO.getPassword()); // It codes automatically

        User savedUser = userService.registerUser(user);

        Map<String, Object> response = new HashMap<>();
        response.put("message", "Sign in success");
        response.put("userId", savedUser.getId());

        return ResponseEntity.ok(response);
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginDTO loginDTO) {
        Optional<User> user = userService.login(loginDTO.getEmail(), loginDTO.getPassword());

        if (user.isPresent()) {
            Map<String, Object> response = new HashMap<>();
            response.put("message", "Login success");
            response.put("user", user.get());
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body("Email or password incorrect");
        }
    }
}