package org.example.task_planner.dto;

import lombok.Data;

@Data
public class UserDTO {
    private String name;
    private String surname;
    private String userId;
    private String email;
    private String password;
}