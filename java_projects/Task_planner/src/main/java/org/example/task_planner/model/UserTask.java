package org.example.task_planner.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "USER_TASKS")
@Data
@NoArgsConstructor
public class UserTask {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "FK_USER_ID")
    private User user;

    @ManyToOne
    @JoinColumn(name = "FK_TASK_ID")
    private Task task;

    @Column(name = "USER_ADMIN")
    private Boolean userAdmin = false;
}