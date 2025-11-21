# Spring Boot 1.x 核心组件功能详解

## 目录
1. [Spring Boot 核心功能](#1-spring-boot-核心功能)
2. [Spring Cloud 微服务组件](#2-spring-cloud-微服务组件)
3. [数据访问组件](#3-数据访问组件)
4. [中间件集成](#4-中间件集成)
5. [监控与管理](#5-监控与管理)
6. [安全与认证](#6-安全与认证)

---

## 1. Spring Boot 核心功能

### 1.1 自动配置（Auto Configuration）
- **位置**: 所有模块的 `@SpringBootApplication` 注解
- **功能**:
  - 自动配置 Spring 应用程序
  - 根据类路径自动配置 Bean
  - 简化 Spring 配置

### 1.2 起步依赖（Starter Dependencies）
- **配置**: `pom.xml` 中的 `spring-boot-starter-*`
- **功能**:
  - `spring-boot-starter-web`: Web 开发
  - `spring-boot-starter-data-redis`: Redis 集成
  - `spring-boot-starter-amqp`: RabbitMQ 集成
  - `spring-boot-starter-actuator`: 监控端点

### 1.3 内嵌服务器
- **默认**: Tomcat
- **配置**: `application.yml` 中的 `server.port`
- **功能**:
  - 无需外部 Web 服务器
  - 支持 JAR 直接运行
  - 简化部署

### 1.4 外部化配置
- **文件**:
  - `application.yml`
  - `bootstrap.yml`
  - Config Server 配置
- **功能**:
  - 多环境配置
  - 配置优先级
  - 动态刷新（@RefreshScope）

---

## 2. Spring Cloud 微服务组件

### 2.1 Eureka - 服务注册与发现

#### 功能特性
- **服务注册**: 服务启动时自动注册到 Eureka
- **服务发现**: 通过服务名调用其他服务
- **健康检查**: 定期心跳检测服务状态
- **负载均衡**: 配合 Ribbon 实现客户端负载均衡

#### 配置示例
```yaml
# Eureka Server 配置
eureka:
  server:
    enable-self-preservation: false  # 关闭自我保护
    eviction-interval-timer-in-ms: 5000  # 清理间隔

# Eureka Client 配置
eureka:
  client:
    service-url:
      defaultZone: http://localhost:18761/eureka/
  instance:
    prefer-ip-address: true
    lease-renewal-interval-in-seconds: 5  # 心跳间隔
```

#### 使用场景
- 微服务架构中的服务治理
- 服务实例动态扩缩容
- 多环境服务隔离

### 2.2 Config Server - 配置中心

#### 功能特性
- **集中管理**: 统一管理所有服务配置
- **版本控制**: 支持 Git 配置仓库
- **动态刷新**: 配置变更无需重启
- **多环境**: dev/test/prod 配置隔离

#### 配置示例
```yaml
# Config Server
spring:
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/config-repo

# Config Client
spring:
  cloud:
    config:
      discovery:
        enabled: true
        service-id: enterprise-config-server
```

#### 使用场景
- 多服务配置统一管理
- 配置变更实时生效
- 敏感信息加密存储

### 2.3 Zuul - API 网关

#### 功能特性
- **路由转发**: 统一入口，路由到后端服务
- **负载均衡**: 集成 Ribbon 实现负载均衡
- **过滤器**: 认证、限流、日志等
- **熔断降级**: 集成 Hystrix

#### 核心组件
```java
// 认证过滤器
@Component
public class AuthFilter extends ZuulFilter {
    @Override
    public String filterType() {
        return "pre";  // 路由前执行
    }

    @Override
    public int filterOrder() {
        return 1;  // 过滤器顺序
    }

    @Override
    public boolean shouldFilter() {
        // 是否执行过滤器
        return true;
    }

    @Override
    public Object run() {
        // 过滤器逻辑
        return null;
    }
}
```

#### 配置示例
```yaml
zuul:
  prefix: /api
  routes:
    user-service:
      path: /user/**
      service-id: enterprise-user-service
```

#### 使用场景
- 统一 API 入口
- 统一认证授权
- 请求日志记录
- API 限流

### 2.4 Feign - 声明式服务调用

#### 功能特性
- **声明式**: 通过接口定义调用
- **负载均衡**: 集成 Ribbon
- **熔断降级**: 集成 Hystrix
- **编码简化**: 无需手写 HTTP 调用

#### 使用示例
```java
// Feign 客户端
@FeignClient(name = "enterprise-user-service",
             fallback = UserServiceFallback.class)
public interface UserServiceClient {
    @GetMapping("/user/{id}")
    Result<?> getUser(@PathVariable("id") Long id);
}

// 降级处理
@Component
public class UserServiceFallback implements UserServiceClient {
    @Override
    public Result<?> getUser(Long id) {
        return Result.fail("用户服务暂时不可用");
    }
}
```

#### 配置示例
```yaml
feign:
  hystrix:
    enabled: true  # 启用 Hystrix
  compression:
    request:
      enabled: true  # 请求压缩
```

### 2.5 Ribbon - 负载均衡

#### 功能特性
- **客户端负载均衡**: 在客户端进行负载均衡
- **多种策略**: 轮询、随机、加权等
- **健康检查**: 自动剔除不可用实例
- **重试机制**: 请求失败自动重试

#### 配置示例
```yaml
ribbon:
  ReadTimeout: 5000  # 读超时
  ConnectTimeout: 3000  # 连接超时
  MaxAutoRetries: 1  # 同一实例重试次数
  MaxAutoRetriesNextServer: 1  # 切换实例重试次数
```

#### 负载均衡策略
- `RoundRobinRule`: 轮询（默认）
- `RandomRule`: 随机
- `WeightedResponseTimeRule`: 响应时间加权
- `BestAvailableRule`: 最小并发

### 2.6 Hystrix - 熔断降级

#### 功能特性
- **熔断器**: 防止故障扩散
- **服务降级**: 提供默认响应
- **请求缓存**: 减少重复请求
- **请求合并**: 批量请求优化

#### 配置示例
```yaml
hystrix:
  command:
    default:
      execution:
        isolation:
          thread:
            timeoutInMilliseconds: 5000  # 超时时间
      circuitBreaker:
        requestVolumeThreshold: 20  # 触发熔断的最小请求数
        errorThresholdPercentage: 50  # 错误率阈值
        sleepWindowInMilliseconds: 5000  # 熔断持续时间
```

#### 使用示例
```java
@HystrixCommand(fallbackMethod = "getUserFallback")
public User getUser(Long id) {
    return userService.getUser(id);
}

public User getUserFallback(Long id) {
    return new User();  // 降级响应
}
```

---

## 3. 数据访问组件

### 3.1 MyBatis

#### 功能特性
- **ORM 映射**: Java 对象与数据库映射
- **动态 SQL**: XML 方式编写复杂 SQL
- **插件机制**: 分页、性能监控等
- **缓存机制**: 一级、二级缓存

#### 配置示例
```yaml
mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.enterprise.user.entity
  configuration:
    map-underscore-to-camel-case: true  # 下划线转驼峰
    cache-enabled: true  # 启用二级缓存
```

#### 使用示例
```java
@Mapper
public interface UserMapper {
    User selectById(Long id);
    int insert(User user);
    int update(User user);
    int deleteById(Long id);
}
```

### 3.2 Druid - 数据库连接池

#### 功能特性
- **高性能**: 优秀的连接池性能
- **监控统计**: SQL 监控、慢 SQL 分析
- **防 SQL 注入**: 内置防火墙
- **扩展性**: 丰富的过滤器

#### 配置示例
```yaml
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    druid:
      initial-size: 5
      min-idle: 5
      max-active: 20
      max-wait: 60000
      validation-query: SELECT 1
```

#### 监控界面
- 访问: `http://localhost:port/druid/`
- 功能: SQL 监控、连接池状态、慢 SQL 分析

---

## 4. 中间件集成

### 4.1 Redis

#### 功能特性
- **缓存**: 减少数据库压力
- **分布式锁**: 解决并发问题
- **Session 共享**: 多实例会话共享
- **消息队列**: 发布订阅模式

#### 使用示例
```java
@Autowired
private RedisTemplate<String, Object> redisTemplate;

// 缓存操作
public void setCache(String key, Object value) {
    redisTemplate.opsForValue().set(key, value, 1, TimeUnit.HOURS);
}

public Object getCache(String key) {
    return redisTemplate.opsForValue().get(key);
}
```

#### 配置示例
```yaml
spring:
  redis:
    host: localhost
    port: 16379
    database: 0
    timeout: 3000
    jedis:
      pool:
        max-active: 8
        max-idle: 8
```

### 4.2 RabbitMQ

#### 功能特性
- **异步处理**: 解耦业务流程
- **流量削峰**: 缓冲高并发请求
- **消息可靠**: 持久化、确认机制
- **灵活路由**: 交换机、队列、绑定

#### 使用示例
```java
// 发送消息
@Autowired
private RabbitTemplate rabbitTemplate;

public void sendMessage(String message) {
    rabbitTemplate.convertAndSend("exchange", "routingKey", message);
}

// 接收消息
@RabbitListener(queues = "queueName")
public void receiveMessage(String message) {
    // 处理消息
}
```

#### 配置示例
```yaml
spring:
  rabbitmq:
    host: localhost
    port: 25672
    username: admin
    password: admin123
    virtual-host: /
```

---

## 5. 监控与管理

### 5.1 Spring Boot Actuator

#### 功能特性
- **健康检查**: `/health` 端点
- **指标监控**: `/metrics` 端点
- **环境信息**: `/env` 端点
- **日志管理**: `/loggers` 端点

#### 常用端点
- `/actuator/health`: 健康状态
- `/actuator/info`: 应用信息
- `/actuator/metrics`: 性能指标
- `/actuator/env`: 环境变量
- `/actuator/beans`: Bean 列表

#### 配置示例
```yaml
management:
  security:
    enabled: false  # 关闭端点安全（开发环境）
  endpoints:
    web:
      exposure:
        include: '*'  # 暴露所有端点
```

### 5.2 Spring Boot Admin

#### 功能特性
- **应用监控**: 可视化监控面板
- **JVM 监控**: 内存、线程、GC
- **日志查看**: 在线查看日志
- **配置查看**: 查看应用配置

#### 访问界面
- URL: `http://localhost:18090`
- 功能:
  - 应用列表
  - 健康状态
  - JVM 信息
  - 日志文件
  - 配置属性

---

## 6. 安全与认证

### 6.1 JWT 认证

#### 功能特性
- **无状态**: 不依赖 Session
- **跨域**: 支持跨域认证
- **安全**: 签名验证
- **灵活**: 自定义载荷

#### 实现示例
```java
// 生成 Token
public String generateToken(String username) {
    return Jwts.builder()
        .setSubject(username)
        .setIssuedAt(new Date())
        .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
        .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
        .compact();
}

// 验证 Token
public boolean validateToken(String token) {
    try {
        Jwts.parser().setSigningKey(SECRET_KEY).parseClaimsJws(token);
        return true;
    } catch (Exception e) {
        return false;
    }
}
```

### 6.2 网关鉴权

#### 实现方式
- Zuul Pre Filter 中验证 Token
- 提取用户信息传递给下游服务
- 统一异常处理

---

## 7. 组件协作流程

### 7.1 服务调用流程
```
客户端 → Zuul 网关 → Ribbon 负载均衡 → Feign 调用 → 目标服务
         ↓
      AuthFilter（认证）
         ↓
      Hystrix（熔断）
```

### 7.2 配置加载流程
```
服务启动 → 读取 bootstrap.yml → 连接 Eureka
                                  ↓
                          查找 Config Server
                                  ↓
                          加载远程配置
                                  ↓
                          合并本地配置
                                  ↓
                          应用配置启动
```

### 7.3 服务注册流程
```
服务启动 → 连接 Eureka Server → 发送注册信息
                                  ↓
                          Eureka 保存实例信息
                                  ↓
                          定期发送心跳
                                  ↓
                          其他服务可发现
```

---

## 8. 最佳实践

### 8.1 服务拆分原则
- 单一职责
- 高内聚低耦合
- 业务边界清晰

### 8.2 配置管理
- 敏感信息加密
- 环境隔离
- 版本控制

### 8.3 熔断降级策略
- 合理设置超时时间
- 提供有意义的降级响应
- 监控熔断指标

### 8.4 缓存策略
- 热点数据缓存
- 设置合理过期时间
- 缓存穿透防护

---

## 9. 常见问题排查

### 9.1 服务调用失败
- 检查 Eureka 注册状态
- 验证服务名配置
- 查看 Ribbon 超时设置
- 检查 Hystrix 熔断状态

### 9.2 配置加载失败
- 确认 Config Server 启动
- 检查 bootstrap.yml 配置
- 验证配置文件路径

### 9.3 性能问题
- 查看慢 SQL（Druid 监控）
- 检查缓存命中率
- 分析 JVM 内存使用
- 查看线程池状态

---

## 10. 参考资料

- [Spring Boot 1.5.x 官方文档](https://docs.spring.io/spring-boot/docs/1.5.x/reference/html/)
- [Spring Cloud Edgware 文档](https://cloud.spring.io/spring-cloud-static/Edgware.SR6/)
- [MyBatis 官方文档](https://mybatis.org/mybatis-3/zh/index.html)
- [Druid 官方文档](https://github.com/alibaba/druid/wiki)
