package com.enterprise.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.circuitbreaker.EnableCircuitBreaker;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.cloud.netflix.feign.EnableFeignClients;

/**
 * 订单服务启动类
 */
@EnableCircuitBreaker
@EnableFeignClients
@EnableEurekaClient
@SpringBootApplication(scanBasePackages = {"com.enterprise.order", "com.enterprise.common"})
public class OrderServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
        System.out.println("========================================");
        System.out.println("Order Service 启动成功！");
        System.out.println("访问地址: http://localhost:18082");
        System.out.println("Swagger文档: http://localhost:18082/swagger-ui.html");
        System.out.println("========================================");
    }

}
