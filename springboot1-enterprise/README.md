# Spring Boot 1.x 企业级多项目框架基座

## 项目概述

这是一个基于 Spring Boot 1.5.22 和 Spring Cloud Edgware.SR6 构建的企业级微服务框架，包含完整的服务治理、配置中心、API网关、监控等功能。

## 技术栈

### 核心框架
- **Spring Boot**: 1.5.22.RELEASE
- **Spring Cloud**: Edgware.SR6
- **JDK**: 1.8

### 微服务组件
- **Eureka**: 服务注册与发现
- **Config Server**: 配置中心
- **Zuul**: API 网关
- **Feign**: 声明式服务调用
- **Ribbon**: 客户端负载均衡
- **Hystrix**: 熔断降级
- **Spring Boot Admin**: 服务监控

### 中间件
- **MySQL**: 5.7（端口: 13306）
- **Redis**: 5.0（端口: 16379）
- **RabbitMQ**: 3.8（端口: 15672/25672）

### 其他组件
- **MyBatis**: ORM 框架
- **Druid**: 数据库连接池
- **Swagger**: API 文档
- **JWT**: 认证授权
- **Lombok**: 简化代码

## 项目结构

```
springboot1-enterprise/
├── enterprise-common/              # 通用模块
│   ├── response/                   # 统一响应对象
│   ├── exception/                  # 全局异常处理
│   └── util/                       # 工具类（JWT等）
├── enterprise-eureka/              # Eureka 注册中心（端口: 18761）
├── enterprise-config/              # 配置中心（端口: 18888）
├── enterprise-gateway/             # API 网关（端口: 18080）
├── enterprise-admin/               # 监控中心（端口: 18090）
├── enterprise-user-service/        # 用户服务（端口: 18081）
├── enterprise-order-service/       # 订单服务（端口: 18082）
└── docker/                         # Docker 编排文件
    ├── docker-compose.yml          # 中间件容器编排
    └── init-sql/                   # MySQL 初始化脚本
```

## 端口规划（所有端口均为非常用端口，适合远程服务器部署）

| 服务名称 | 端口 | 说明 |
|---------|------|------|
| Eureka Server | 18761 | 服务注册中心 |
| Config Server | 18888 | 配置中心 |
| API Gateway | 18080 | API 网关 |
| Admin Server | 18090 | 监控中心 |
| User Service | 18081 | 用户服务 |
| Order Service | 18082 | 订单服务 |
| MySQL | 13306 | 数据库 |
| Redis | 16379 | 缓存 |
| RabbitMQ管理 | 15672 | 消息队列管理界面 |
| RabbitMQ | 25672 | 消息队列AMQP |

## 快速开始

### 1. 环境准备

- JDK 1.8+
- Maven 3.3+
- Docker & Docker Compose

### 2. 启动中间件

```bash
# 进入 docker 目录
cd docker

# 启动所有中间件（MySQL、Redis、RabbitMQ）
docker-compose up -d

# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

中间件访问地址：
- MySQL: `localhost:13306` (用户名: root, 密码: root123)
- Redis: `localhost:16379`
- RabbitMQ管理界面: http://localhost:15672 (用户名: admin, 密码: admin123)

### 3. 编译项目

```bash
# 在项目根目录执行
mvn clean install -DskipTests
```

### 4. 启动服务（按顺序）

**方式一：使用 Maven 启动（开发环境）**

```bash
# 1. 启动 Eureka 注册中心
cd enterprise-eureka
mvn spring-boot:run

# 2. 启动配置中心
cd ../enterprise-config
mvn spring-boot:run

# 3. 启动 API 网关
cd ../enterprise-gateway
mvn spring-boot:run

# 4. 启动监控中心
cd ../enterprise-admin
mvn spring-boot:run

# 5. 启动用户服务
cd ../enterprise-user-service
mvn spring-boot:run

# 6. 启动订单服务
cd ../enterprise-order-service
mvn spring-boot:run
```

**方式二：使用 JAR 包启动（生产环境）**

```bash
# 1. 启动 Eureka
java -jar enterprise-eureka/target/enterprise-eureka-1.0.0-SNAPSHOT.jar

# 2. 启动 Config Server
java -jar enterprise-config/target/enterprise-config-1.0.0-SNAPSHOT.jar

# 3. 启动 Gateway
java -jar enterprise-gateway/target/enterprise-gateway-1.0.0-SNAPSHOT.jar

# 4. 启动 Admin
java -jar enterprise-admin/target/enterprise-admin-1.0.0-SNAPSHOT.jar

# 5. 启动 User Service
java -jar enterprise-user-service/target/enterprise-user-service-1.0.0-SNAPSHOT.jar

# 6. 启动 Order Service
java -jar enterprise-order-service/target/enterprise-order-service-1.0.0-SNAPSHOT.jar
```

### 5. 访问服务

| 服务 | 访问地址 | 说明 |
|-----|---------|------|
| Eureka 控制台 | http://localhost:18761 | 查看服务注册情况 |
| Config Server | http://localhost:18888/application/default | 配置中心 |
| Admin 监控 | http://localhost:18090 | 服务监控面板 |
| 用户服务 API | http://localhost:18081/swagger-ui.html | 用户服务文档 |
| 订单服务 API | http://localhost:18082/swagger-ui.html | 订单服务文档 |
| API 网关 | http://localhost:18080/api/ | 统一网关入口 |

## API 测试

### 通过网关访问（推荐）

```bash
# 1. 用户登录
curl -X POST http://localhost:18080/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}'

# 返回 token，用于后续请求

# 2. 获取用户信息
curl -X GET http://localhost:18080/api/user/1 \
  -H "Authorization: YOUR_TOKEN"

# 3. 创建订单
curl -X POST http://localhost:18080/api/order/create \
  -H "Content-Type: application/json" \
  -H "Authorization: YOUR_TOKEN" \
  -d '{
    "userId": 1,
    "productName": "测试商品",
    "quantity": 2,
    "amount": 199.99
  }'

# 4. 获取订单详情（含用户信息，演示Feign服务调用）
curl -X GET http://localhost:18080/api/order/1/detail \
  -H "Authorization: YOUR_TOKEN"
```

### 直接访问服务

```bash
# 用户服务健康检查
curl http://localhost:18081/user/health

# 订单服务健康检查
curl http://localhost:18082/order/health
```

## Spring Boot 1.x 核心组件功能

### 1. 服务注册与发现（Eureka）
- 服务自动注册
- 服务健康检查
- 服务负载均衡
- 服务故障剔除

### 2. 配置中心（Config Server）
- 集中配置管理
- 配置动态刷新
- 多环境配置支持
- 本地/Git 配置仓库

### 3. API 网关（Zuul）
- 路由转发
- 负载均衡
- 认证授权过滤
- 请求限流

### 4. 服务调用（Feign + Ribbon）
- 声明式 REST 客户端
- 客户端负载均衡
- 服务间通信简化

### 5. 熔断降级（Hystrix）
- 服务熔断
- 服务降级
- 请求缓存
- 请求合并

### 6. 服务监控（Spring Boot Admin）
- 应用健康监控
- JVM 信息监控
- 日志查看
- 配置查看

### 7. 数据访问（MyBatis + Druid）
- ORM 映射
- 数据库连接池
- SQL 监控
- 慢 SQL 分析

### 8. 缓存（Redis）
- 数据缓存
- 分布式锁
- 消息发布订阅

### 9. 消息队列（RabbitMQ）
- 异步消息处理
- 解耦服务依赖
- 流量削峰

### 10. 认证授权（JWT）
- Token 生成与验证
- 无状态认证
- 网关统一鉴权

### 11. API 文档（Swagger）
- 自动生成 API 文档
- 在线接口测试
- 接口参数说明

## 开发指南

### 添加新服务

1. 在父 POM 中添加模块
2. 创建服务模块，引入必要依赖
3. 配置 Eureka、Config Client
4. 实现业务逻辑
5. 在网关中配置路由

### 配置管理

配置文件位置：`enterprise-config/src/main/resources/config-repo/`

- `application.yml`: 公共配置
- `{service-name}.yml`: 服务专属配置

### 数据库迁移

SQL 脚本位置：`docker/init-sql/`

修改后需要重建 MySQL 容器：
```bash
docker-compose down
rm -rf docker/data/mysql
docker-compose up -d mysql
```

## 常见问题

### 1. 服务无法注册到 Eureka
- 检查 Eureka 是否启动
- 检查网络连接
- 查看服务日志

### 2. 配置中心无法获取配置
- 确保 Config Server 先于其他服务启动
- 检查 bootstrap.yml 配置
- 验证配置文件路径

### 3. 网关路由失败
- 检查服务是否注册成功
- 验证 Zuul 路由配置
- 查看网关日志

### 4. Docker 容器启动失败
- 检查端口是否被占用
- 查看容器日志：`docker-compose logs`
- 确保 Docker 服务正常运行

## 生产部署建议

1. **服务高可用**：每个服务至少部署 2 个实例
2. **Eureka 集群**：部署多个 Eureka 节点互相注册
3. **配置外部化**：使用 Git 仓库管理配置
4. **日志集中化**：集成 ELK 日志系统
5. **监控告警**：集成 Prometheus + Grafana
6. **数据库主从**：配置 MySQL 主从复制
7. **Redis 集群**：部署 Redis Cluster 或哨兵模式
8. **限流熔断**：合理配置 Hystrix 参数

## 版本说明

- Spring Boot 1.5.22 是 1.x 系列最后一个稳定版本
- Spring Cloud Edgware.SR6 与 Spring Boot 1.5.x 完美适配
- 该版本适合学习和维护老项目，新项目建议使用 Spring Boot 2.x/3.x

## 参考文档

- [Spring Boot 1.5.x 官方文档](https://docs.spring.io/spring-boot/docs/1.5.x/reference/html/)
- [Spring Cloud Edgware 官方文档](https://cloud.spring.io/spring-cloud-static/Edgware.SR6/)
- [Eureka 使用指南](https://github.com/Netflix/eureka/wiki)
- [Zuul 使用指南](https://github.com/Netflix/zuul/wiki)

## 许可证

MIT License

---

**作者**: Enterprise Team
**日期**: 2024
**联系**: 如有问题请提交 Issue
