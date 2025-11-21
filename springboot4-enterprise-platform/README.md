# Spring Boot 4.x Enterprise Platform

企业级多项目Spring Boot 4.x框架基座 - 基于Spring Framework 7和最新企业级技术栈

## 项目概述

这是一个现代化的企业级多模块Spring Boot 4.x平台,采用最新的Spring Framework 7特性,旨在为企业应用提供可扩展、高性能、易维护的基础架构。

### 核心特性

- **Spring Boot 4.x & Spring Framework 7**
  - 内置弹性机制 (@Retryable, @ConcurrencyLimit)
  - API版本控制支持
  - JSpecify空安全
  - 虚拟线程支持(Project Loom)
  - Jackson 3.x JSON处理

- **企业级架构**
  - 多模块Maven项目结构
  - 领域驱动设计(DDD)
  - 微服务就绪
  - 统一异常处理
  - 统一响应格式

- **安全认证**
  - JWT Token认证
  - Spring Security 7.x
  - OAuth2资源服务器
  - RBAC权限控制

- **数据访问**
  - Spring Data JPA
  - MyBatis支持
  - 多数据源支持
  - HikariCP连接池

- **缓存与消息**
  - Redis (Redisson)
  - RabbitMQ
  - Apache Kafka

- **可观测性**
  - Spring Boot Actuator
  - Prometheus监控
  - Grafana可视化
  - 分布式追踪

- **GraalVM原生镜像**
  - AOT编译支持
  - 快速启动
  - 低内存占用

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 21 | LTS版本,支持虚拟线程 |
| Spring Boot | 4.0.0-M2 | 最新里程碑版本 |
| Spring Framework | 7.0.0-M3 | 内置弹性、API版本控制 |
| Spring Security | 7.x | 认证授权 |
| MySQL | 9.1 | 主数据库 |
| PostgreSQL | 17 | 备选数据库 |
| Redis | 7.4 | 缓存 |
| RabbitMQ | 4.0 | 消息队列 |
| Kafka | 3.9 | 流处理 |
| Prometheus | Latest | 指标采集 |
| Grafana | Latest | 可视化 |

## 项目结构

```
springboot4-enterprise-platform/
├── platform-common/                 # 通用模块
│   ├── common-core/                # 核心工具、常量
│   ├── common-domain/              # 领域模型、DTO
│   └── common-exception/           # 统一异常处理
├── platform-framework/             # 框架层
│   ├── framework-security/         # 安全认证框架
│   ├── framework-data/             # 数据访问框架
│   ├── framework-cache/            # 缓存框架
│   ├── framework-mq/               # 消息队列框架
│   ├── framework-resilience/       # 弹性框架
│   └── framework-observability/    # 可观测性框架
├── platform-services/              # 业务服务
│   ├── service-user/               # 用户服务
│   ├── service-order/              # 订单服务
│   └── service-product/            # 产品服务
├── platform-api/                   # API网关
│   └── api-gateway/                # 统一网关
├── platform-admin/                 # 管理后台
└── docker-compose/                 # Docker编排配置
```

## 快速开始

### 环境要求

- JDK 21+
- Maven 3.9+
- Docker & Docker Compose

### 1. 启动中间件服务

```bash
cd docker-compose
docker-compose up -d
```

这将启动以下服务:
- MySQL (端口: 3306)
- PostgreSQL (端口: 5432)
- Redis (端口: 6379)
- RabbitMQ (端口: 5672, 管理界面: 15672)
- Kafka (端口: 9092)
- Prometheus (端口: 9090)
- Grafana (端口: 3000)

### 2. 编译项目

```bash
mvn clean install
```

### 3. 运行用户服务

```bash
cd platform-services/service-user
mvn spring-boot:run
```

服务将在 `http://localhost:8081` 启动

### 4. 访问监控面板

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **RabbitMQ**: http://localhost:15672 (admin/password)

## 模块说明

### Common模块

#### common-core
- 统一响应结果封装 (Result, PageResult)
- 常用工具类 (JsonUtils, IdGenerator)
- 全局常量定义

#### common-exception
- 全局异常处理器
- 自定义异常类
- 统一错误码

### Framework模块

#### framework-security
- JWT Token生成与验证
- Spring Security配置
- 认证过滤器
- 权限控制

#### framework-data
- JPA配置
- MyBatis配置
- 多数据源支持
- 事务管理

#### framework-cache
- Redis缓存配置
- Redisson客户端
- 缓存注解

#### framework-mq
- RabbitMQ配置
- Kafka配置
- 消息生产者/消费者

#### framework-resilience
- @Retryable重试机制
- @ConcurrencyLimit并发限制
- 熔断器配置

#### framework-observability
- Actuator端点
- Prometheus指标
- 分布式追踪

## Spring Framework 7 新特性使用

### 1. 内置弹性机制

```java
@Service
public class UserService {

    // 自动重试,最多3次
    @Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000))
    public User getUserById(Long id) {
        // 可能失败的操作
    }

    // 限制并发数为10
    @ConcurrencyLimit(10)
    public void processOrder(Order order) {
        // 资源密集型操作
    }
}
```

### 2. API版本控制

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping(version = "v1")
    public Result<User> getUserV1(@PathVariable Long id) {
        // V1 API实现
    }

    @GetMapping(version = "v2")
    public Result<UserDTO> getUserV2(@PathVariable Long id) {
        // V2 API实现
    }
}
```

### 3. JSpecify空安全

```java
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;

public class UserService {

    @Nullable
    public User findUser(Long id) {
        // 可能返回null
    }

    public void saveUser(@NonNull User user) {
        // user不能为null
    }
}
```

## Docker部署

### 构建镜像

```bash
# 构建用户服务镜像
cd platform-services/service-user
mvn spring-boot:build-image
```

### GraalVM原生镜像

```bash
# 构建原生镜像
mvn -Pnative spring-boot:build-image
```

## 配置说明

### application.yml 主要配置

```yaml
# 数据源配置
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/user_db
    username: root
    password: password

# Redis配置
  data:
    redis:
      host: localhost
      port: 6379

# JWT配置
security:
  jwt:
    secret: your-secret-key
    expiration: 86400000  # 24小时
```

## 开发指南

### 创建新服务模块

1. 复制 `service-user` 模块
2. 修改 `pom.xml` 中的 `artifactId`
3. 修改主类名和包名
4. 在父POM中添加模块引用
5. 更新 `application.yml` 配置

### 添加新的实体

```java
@Entity
@Table(name = "users")
@Data
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    // 其他字段...
}
```

### 使用统一响应

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @GetMapping("/{id}")
    public Result<User> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        return Result.success(user);
    }

    @PostMapping
    public Result<User> createUser(@RequestBody @Valid UserDTO dto) {
        User user = userService.create(dto);
        return Result.success(user);
    }
}
```

## 监控与运维

### Actuator端点

- `/actuator/health` - 健康检查
- `/actuator/metrics` - 指标信息
- `/actuator/prometheus` - Prometheus格式指标
- `/actuator/info` - 应用信息

### 日志配置

日志输出在 `application.yml` 中配置:

```yaml
logging:
  level:
    root: INFO
    com.enterprise: DEBUG
```

## 性能优化

### 虚拟线程 (Java 21)

```java
@Configuration
public class AsyncConfig {

    @Bean
    public TaskExecutor taskExecutor() {
        return new SimpleAsyncTaskExecutor("virtual-");
    }
}
```

### 缓存策略

```java
@Service
public class UserService {

    @Cacheable(value = "users", key = "#id")
    public User findById(Long id) {
        return userRepository.findById(id).orElse(null);
    }

    @CacheEvict(value = "users", key = "#user.id")
    public void update(User user) {
        userRepository.save(user);
    }
}
```

## 测试

### 单元测试

```bash
mvn test
```

### 集成测试

```bash
mvn verify
```

## 常见问题

### 1. 数据库连接失败

确保Docker容器已启动:
```bash
docker-compose ps
```

### 2. Redis连接失败

检查Redis服务状态:
```bash
docker logs enterprise-redis
```

### 3. JWT Token无效

确保配置了正确的secret密钥,且长度足够

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

- 项目地址: [GitHub Repository]
- 问题反馈: [Issues]

---

**注意**: 本项目使用Spring Boot 4.x里程碑版本,不建议在生产环境使用。请等待正式版发布。
