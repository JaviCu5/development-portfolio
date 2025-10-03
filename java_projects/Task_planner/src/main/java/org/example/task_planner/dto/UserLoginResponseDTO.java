package org.example.task_planner.dto;

import lombok.Data;
import java.util.List;

@Data
public class UserLoginResponseDTO {
    private Long id;
    private String name;
    private String surname;
    private String userId;
    private String email;
    // No password field!

    // If you want to include task information
    // private List<TaskInfoDTO> tasks;
}