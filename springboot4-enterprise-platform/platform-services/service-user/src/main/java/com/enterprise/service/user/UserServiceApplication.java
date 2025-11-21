package com.enterprise.service.user;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * User Service Application
 * Spring Boot 4.x Application
 */
@SpringBootApplication
@EnableJpaAuditing
@ComponentScan(basePackages = {
        "com.enterprise.service.user",
        "com.enterprise.framework",
        "com.enterprise.common"
})
@EntityScan(basePackages = "com.enterprise.service.user.entity")
@EnableJpaRepositories(basePackages = "com.enterprise.service.user.repository")
public class UserServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}
