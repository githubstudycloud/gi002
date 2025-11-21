# Go 企业级多项目框架基座架构设计

## 项目概述
这是一个完整的 Go 企业级微服务框架基座，包含了企业开发所需的所有核心组件和最佳实践。

## 技术栈

### 核心框架
- **Go 1.21+**: 编程语言
- **Gin**: HTTP Web 框架
- **gRPC**: 微服务通信框架
- **Wire**: 依赖注入

### 数据存储
- **MySQL**: 关系型数据库
- **PostgreSQL**: 关系型数据库
- **MongoDB**: NoSQL 数据库
- **Redis**: 缓存和会话存储
- **Memcached**: 分布式缓存

### 消息队列
- **RabbitMQ**: 消息队列 (端口: 5672, 管理界面: 15672)
- **Kafka**: 分布式流处理平台 (端口: 9092, Zookeeper: 2181)

### 服务治理
- **Consul**: 服务发现和配置中心 (端口: 8500)
- **Etcd**: 分布式键值存储 (端口: 2379, 2380)

### 监控和追踪
- **Prometheus**: 监控系统 (端口: 9090)
- **Grafana**: 可视化面板 (端口: 3000)
- **Jaeger**: 分布式链路追踪 (端口: 16686, 14268, 6831)
- **ELK Stack**: 日志收集分析

### 安全认证
- **JWT**: Token 认证
- **OAuth2**: 授权框架
- **RBAC**: 基于角色的访问控制
- **Casbin**: 权限管理

## 项目结构

```
go-enterprise-platform/
├── cmd/                          # 应用程序入口
│   ├── api-gateway/             # API 网关服务 (端口: 8080)
│   ├── user-service/            # 用户服务 (端口: 8081, gRPC: 9091)
│   └── order-service/           # 订单服务 (端口: 8082, gRPC: 9092)
├── pkg/                         # 可复用的公共包
│   ├── config/                  # 配置管理 (支持 Viper, Consul, Etcd)
│   ├── logger/                  # 日志组件 (Zap)
│   ├── errors/                  # 统一错误处理
│   ├── database/                # 数据库连接池
│   │   ├── mysql/
│   │   ├── postgres/
│   │   └── mongodb/
│   ├── cache/                   # 缓存组件
│   │   ├── redis/
│   │   └── memcached/
│   ├── mq/                      # 消息队列
│   │   ├── rabbitmq/
│   │   └── kafka/
│   ├── registry/                # 服务注册发现
│   │   ├── consul/
│   │   └── etcd/
│   ├── http/                    # HTTP 服务封装
│   │   ├── gin/
│   │   └── middleware/
│   ├── grpc/                    # gRPC 服务封装
│   ├── auth/                    # 认证授权
│   │   ├── jwt/
│   │   ├── oauth2/
│   │   └── rbac/
│   └── monitoring/              # 监控追踪
│       ├── prometheus/
│       └── jaeger/
├── internal/                    # 私有应用代码
│   ├── user/                    # 用户服务业务逻辑
│   │   ├── handler/            # HTTP 处理器
│   │   ├── service/            # 业务服务
│   │   ├── repository/         # 数据访问层
│   │   └── model/              # 数据模型
│   └── order/                   # 订单服务业务逻辑
│       ├── handler/
│       ├── service/
│       ├── repository/
│       └── model/
├── api/                         # API 定义
│   ├── proto/                   # gRPC protobuf 定义
│   └── http/                    # HTTP API 文档
├── deployments/                 # 部署配置
│   ├── docker/                  # Docker 配置
│   │   └── docker-compose.yml  # 中间件编排
│   └── kubernetes/              # K8s 配置
├── scripts/                     # 脚本工具
│   ├── init.sh                 # 初始化脚本
│   └── test-services.sh        # 服务测试脚本
├── docs/                        # 文档
├── test/                        # 集成测试
├── go.mod                       # Go 模块定义
├── go.sum
├── Makefile                     # 构建脚本
└── README.md                    # 项目说明

```

## 端口分配规划

### 应用服务
- API Gateway: 8080
- User Service HTTP: 8081
- User Service gRPC: 9091
- Order Service HTTP: 8082
- Order Service gRPC: 9092

### 中间件服务
- MySQL: 3306
- PostgreSQL: 5432
- MongoDB: 27017
- Redis: 6379
- Memcached: 11211
- RabbitMQ: 5672 (管理界面: 15672)
- Kafka: 9092
- Zookeeper: 2181
- Consul: 8500
- Etcd: 2379, 2380
- Prometheus: 9090
- Grafana: 3000
- Jaeger UI: 16686
- Jaeger Collector: 14268
- Jaeger Agent: 6831

## 核心功能特性

### 1. 配置管理
- 支持多环境配置 (dev, test, prod)
- 支持配置热更新
- 支持远程配置中心 (Consul, Etcd)
- 支持环境变量覆盖

### 2. 日志系统
- 结构化日志 (JSON)
- 日志级别控制
- 日志轮转
- 分布式日志追踪 (Trace ID)

### 3. 数据库
- 连接池管理
- 读写分离
- 主从切换
- 慢查询监控
- ORM 支持 (GORM)

### 4. 缓存
- 多级缓存
- 缓存预热
- 缓存击穿防护
- 缓存雪崩防护

### 5. 消息队列
- 消息持久化
- 消息重试
- 死信队列
- 消息追踪

### 6. 服务治理
- 服务注册与发现
- 健康检查
- 负载均衡
- 服务熔断
- 服务限流

### 7. 监控告警
- 性能指标采集
- 业务指标统计
- 链路追踪
- 日志聚合
- 告警通知

### 8. 安全
- JWT 认证
- OAuth2 授权
- RBAC 权限控制
- API 限流
- XSS/CSRF 防护
- SQL 注入防护

## 开发规范

### 代码规范
- 遵循 Go 官方代码规范
- 使用 golangci-lint 进行代码检查
- 代码覆盖率 > 80%

### API 规范
- RESTful API 设计
- 统一响应格式
- 统一错误码
- API 版本控制

### Git 规范
- 分支管理 (Git Flow)
- Commit Message 规范
- Code Review 流程

## 快速开始

### 前置要求
- Go 1.21+
- Docker & Docker Compose
- Make

### 启动步骤
1. 初始化项目依赖
2. 启动中间件服务
3. 启动微服务
4. 运行测试

详细步骤请查看 README.md
