package com.enterprise.job.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.quartz.SchedulerFactoryBean;

import javax.sql.DataSource;
import java.util.Properties;

/**
 * Quartz配置类
 */
@Configuration
@EnableScheduling
public class QuartzConfig {

    /**
     * Scheduler工厂
     */
    @Bean
    public SchedulerFactoryBean schedulerFactoryBean(DataSource dataSource) {
        SchedulerFactoryBean factory = new SchedulerFactoryBean();
        factory.setDataSource(dataSource);
        factory.setQuartzProperties(quartzProperties());
        // 延迟启动
        factory.setStartupDelay(10);
        // 应用启动时自动启动
        factory.setAutoStartup(true);
        // 覆盖已存在的任务
        factory.setOverwriteExistingJobs(true);
        // 优雅关闭
        factory.setWaitForJobsToCompleteOnShutdown(true);
        return factory;
    }

    /**
     * Quartz属性配置
     */
    private Properties quartzProperties() {
        Properties properties = new Properties();
        // 调度器实例名
        properties.put("org.quartz.scheduler.instanceName", "EnterpriseScheduler");
        properties.put("org.quartz.scheduler.instanceId", "AUTO");

        // 线程池配置
        properties.put("org.quartz.threadPool.class", "org.quartz.simpl.SimpleThreadPool");
        properties.put("org.quartz.threadPool.threadCount", "10");
        properties.put("org.quartz.threadPool.threadPriority", "5");

        // JobStore配置 (数据库存储)
        properties.put("org.quartz.jobStore.class", "org.springframework.scheduling.quartz.LocalDataSourceJobStore");
        properties.put("org.quartz.jobStore.driverDelegateClass", "org.quartz.impl.jdbcjobstore.StdJDBCDelegate");
        properties.put("org.quartz.jobStore.tablePrefix", "QRTZ_");
        properties.put("org.quartz.jobStore.isClustered", "true");
        properties.put("org.quartz.jobStore.clusterCheckinInterval", "10000");
        properties.put("org.quartz.jobStore.useProperties", "false");
        properties.put("org.quartz.jobStore.misfireThreshold", "60000");

        return properties;
    }
}
