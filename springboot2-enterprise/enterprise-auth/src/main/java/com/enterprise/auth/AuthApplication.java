package com.enterprise.auth;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

/**
 * 认证授权服务启动类
 */
@EnableDiscoveryClient
@SpringBootApplication(scanBasePackages = "com.enterprise")
public class AuthApplication {

    public static void main(String[] args) {
        SpringApplication.run(AuthApplication.class, args);
        System.out.println("===============================================");
        System.out.println("      认证授权服务启动成功 - 端口: 9200        ");
        System.out.println("===============================================");
    }
}
