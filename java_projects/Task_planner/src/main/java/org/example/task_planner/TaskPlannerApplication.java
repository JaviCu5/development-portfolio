package org.example.task_planner;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TaskPlannerApplication {

    public static void main(String[] args) {
        SpringApplication.run(TaskPlannerApplication.class, args);
    }

    /*
    @Bean
    public CommandLineRunner demo(TaskRepository taskRepository) {
        return (args) -> {
            // Creates some examples
            Task task1 = new Task();
            task1.setTitle("Example task");
            task1.setDescription("This is a task created automatically");
            task1.setIsCompleted(false);

            taskRepository.save(task1);
            System.out.println("Task saved on database!");
        };
    }*/
}