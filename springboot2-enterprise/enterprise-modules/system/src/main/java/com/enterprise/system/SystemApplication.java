package com.enterprise.system;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

/**
 * 系统管理服务启动类
 */
@EnableDiscoveryClient
@SpringBootApplication(scanBasePackages = "com.enterprise")
@MapperScan("com.enterprise.system.mapper")
public class SystemApplication {

    public static void main(String[] args) {
        SpringApplication.run(SystemApplication.class, args);
        System.out.println("===============================================");
        System.out.println("      系统管理服务启动成功 - 端口: 9201        ");
        System.out.println("===============================================");
    }
}
