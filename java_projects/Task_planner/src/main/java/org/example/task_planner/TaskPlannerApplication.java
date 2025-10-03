package org.example.task_planner;

import org.example.task_planner.model.Task;
import org.example.task_planner.repository.TaskRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class TaskPlannerApplication {

    public static void main(String[] args) {
        SpringApplication.run(TaskPlannerApplication.class, args);
    }

    /*
    @Bean
    public CommandLineRunner demo(TaskRepository taskRepository) {
        return (args) -> {
            // Crear algunas tareas de ejemplo
            Task task1 = new Task();
            task1.setTitle("Tarea de ejemplo");
            task1.setDescription("Esta es una tarea creada automáticamente");
            task1.setIsCompleted(false);

            taskRepository.save(task1);
            System.out.println("Tarea guardada en la base de datos!");
        };
    }*/
}