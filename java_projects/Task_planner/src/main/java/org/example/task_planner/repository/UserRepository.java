package org.example.task_planner.repository;

import org.example.task_planner.dto.UserLoginResponseDTO;
import org.example.task_planner.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    Optional<UserLoginResponseDTO> findByEmailLogin(String email);
    Optional<User> findByUserId(String userId);
    Boolean existsByEmail(String email);
    Boolean existsByUserId(String userId);
}