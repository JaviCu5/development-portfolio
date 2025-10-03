package org.example.task_planner.repository;

import org.example.task_planner.model.Task;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

    // Consultas personalizadas
    List<Task> findByIsCompleted(Boolean isCompleted);
    List<Task> findByTitleContainingIgnoreCase(String title);
}