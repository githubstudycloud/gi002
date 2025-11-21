# Go 企业级多项目框架基座

一个功能完整、可扩展的 Go 企业级微服务框架，集成了现代企业开发所需的所有核心组件和最佳实践。

## 特性

### 核心功能
- ✅ **配置管理**: 支持多环境配置、配置热更新、远程配置中心 (Viper)
- ✅ **日志系统**: 结构化日志、日志级别控制、日志轮转 (Zap)
- ✅ **错误处理**: 统一错误码、错误链追踪
- ✅ **依赖注入**: 基于 Wire 的依赖注入

### 数据存储
- ✅ **MySQL**: 连接池管理、GORM 支持
- ✅ **PostgreSQL**: 连接池管理、GORM 支持
- ✅ **MongoDB**: 官方驱动、连接池管理

### 缓存
- ✅ **Redis**: 完整的 Redis 客户端封装
- ✅ **Memcached**: Memcached 客户端支持

### 消息队列
- ✅ **RabbitMQ**: Docker 配置、管理界面
- ✅ **Kafka**: 与 Zookeeper 集成

### 服务治理
- ✅ **Consul**: 服务注册与发现、配置中心
- ✅ **Etcd**: 分布式配置存储

### Web 框架
- ✅ **Gin**: HTTP 服务框架、中间件支持
- ⏳ **gRPC**: 微服务通信 (待完善)

### 监控追踪
- ✅ **Prometheus**: 指标采集、监控告警
- ✅ **Grafana**: 数据可视化面板
- ✅ **Jaeger**: 分布式链路追踪

### 安全
- ⏳ **JWT**: Token 认证 (待完善)
- ⏳ **OAuth2**: 授权框架 (待完善)
- ⏳ **RBAC**: 基于角色的访问控制 (待完善)

## 项目结构

```
go-enterprise-platform/
├── cmd/                          # 应用程序入口
│   ├── api-gateway/             # API 网关 (端口: 8080)
│   ├── user-service/            # 用户服务 (HTTP: 8081, gRPC: 9091)
│   └── order-service/           # 订单服务 (HTTP: 8082, gRPC: 9092)
├── pkg/                         # 可复用的公共包
│   ├── config/                  # 配置管理
│   ├── logger/                  # 日志组件
│   ├── errors/                  # 错误处理
│   ├── database/                # 数据库连接
│   │   ├── mysql/
│   │   ├── postgres/
│   │   └── mongodb/
│   ├── cache/                   # 缓存组件
│   │   ├── redis/
│   │   └── memcached/
│   ├── mq/                      # 消息队列 (待实现)
│   ├── registry/                # 服务注册发现 (待实现)
│   ├── http/                    # HTTP 服务
│   │   └── gin/
│   ├── grpc/                    # gRPC 服务 (待实现)
│   ├── auth/                    # 认证授权 (待实现)
│   └── monitoring/              # 监控追踪 (待实现)
├── internal/                    # 私有应用代码
│   └── user/                    # 用户服务业务逻辑
│       ├── handler/            # HTTP 处理器
│       ├── service/            # 业务服务
│       ├── repository/         # 数据访问层
│       └── model/              # 数据模型
├── api/                         # API 定义
│   ├── proto/                   # gRPC protobuf 定义
│   └── http/                    # HTTP API 文档
├── deployments/                 # 部署配置
│   └── docker/                  # Docker 配置
│       ├── docker-compose.yml  # 中间件编排
│       └── prometheus.yml      # Prometheus 配置
├── scripts/                     # 脚本工具
│   ├── start-services.sh       # 启动中间件脚本
│   └── test-services.sh        # 测试服务连接脚本
├── config/                      # 配置文件
│   └── config-dev.yaml         # 开发环境配置
├── docs/                        # 文档
├── test/                        # 集成测试
├── ARCHITECTURE.md              # 架构设计文档
├── Makefile                     # 构建脚本
└── README.md                    # 项目说明
```

## 端口分配

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
- RabbitMQ AMQP: 5672
- RabbitMQ 管理界面: 15672
- Kafka: 9092
- Zookeeper: 2181
- Consul: 8500
- Etcd: 2379, 2380
- Prometheus: 9090
- Grafana: 3000
- Jaeger UI: 16686
- Jaeger Collector: 14268
- Jaeger Agent: 6831

## 快速开始

### 前置要求
- Go 1.21 或更高版本
- Docker 和 Docker Compose
- Make (可选)

### 1. 克隆项目

```bash
cd go-enterprise-platform
```

### 2. 启动中间件服务

使用 Docker Compose 启动所有中间件：

```bash
# 使用脚本启动
bash scripts/start-services.sh

# 或手动启动
cd deployments/docker
docker-compose up -d
```

等待所有服务启动完成（约 30-60 秒）。

### 3. 测试服务连接

```bash
bash scripts/test-services.sh
```

### 4. 安装 Go 依赖

```bash
go mod download
go mod tidy
```

### 5. 运行用户服务

```bash
# 使用 Go 直接运行
go run cmd/user-service/main.go

# 或使用 Makefile
make run-user
```

### 6. 测试 API

用户注册：
```bash
curl -X POST http://localhost:8081/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "nickname": "Test User"
  }'
```

用户登录：
```bash
curl -X POST http://localhost:8081/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

获取用户信息：
```bash
curl http://localhost:8081/api/v1/users/1
```

用户列表：
```bash
curl "http://localhost:8081/api/v1/users?page=1&page_size=10"
```

健康检查：
```bash
curl http://localhost:8081/health
```

## 配置说明

### 配置文件

配置文件位于 `config/` 目录，支持多环境配置：
- `config-dev.yaml`: 开发环境
- `config-test.yaml`: 测试环境
- `config-prod.yaml`: 生产环境

### 环境变量

可以使用环境变量覆盖配置文件中的值：

```bash
export APP_NAME=my-service
export DATABASE_MYSQL_HOST=localhost
export DATABASE_MYSQL_PORT=3306
```

## 开发指南

### 添加新的服务

1. 在 `cmd/` 下创建服务目录
2. 在 `internal/` 下创建业务逻辑
3. 实现 Handler -> Service -> Repository 三层架构
4. 在 `config/config-dev.yaml` 中添加配置
5. 更新端口分配避免冲突

### 代码规范

```bash
# 代码格式化
go fmt ./...

# 代码检查
golangci-lint run ./...

# 运行测试
go test -v ./...
```

### 构建

```bash
# 构建所有服务
make build

# 构建单个服务
go build -o bin/user-service ./cmd/user-service
```

## 监控和调试

### Prometheus 监控
访问 http://localhost:9090 查看 Prometheus 监控面板

### Grafana 可视化
访问 http://localhost:3000 (用户名: admin, 密码: admin123456)

### Jaeger 链路追踪
访问 http://localhost:16686 查看分布式追踪信息

### RabbitMQ 管理界面
访问 http://localhost:15672 (用户名: admin, 密码: admin123456)

### Consul 服务发现
访问 http://localhost:8500 查看 Consul UI

## 中间件凭据

### MySQL
- 主机: localhost:3306
- 用户: appuser
- 密码: apppass123
- 数据库: enterprise_db

### PostgreSQL
- 主机: localhost:5432
- 用户: appuser
- 密码: apppass123
- 数据库: enterprise_db

### MongoDB
- URI: mongodb://admin:admin123456@localhost:27017
- 数据库: enterprise_db

### Redis
- 主机: localhost:6379
- 密码: redis123456
- DB: 0

### RabbitMQ
- 主机: localhost:5672
- 用户: admin
- 密码: admin123456
- 管理界面: http://localhost:15672

## 停止服务

```bash
cd deployments/docker
docker-compose down

# 同时删除数据卷
docker-compose down -v
```

## 故障排查

### 端口冲突
如果遇到端口冲突，修改 `docker-compose.yml` 中的端口映射。

### 服务无法启动
检查 Docker 日志：
```bash
cd deployments/docker
docker-compose logs -f [service-name]
```

### 连接数据库失败
确保 Docker 容器已完全启动：
```bash
docker ps
```

## 架构文档

详细的架构设计请参考 [ARCHITECTURE.md](ARCHITECTURE.md)

## 待实现功能

- [ ] RabbitMQ/Kafka 组件封装
- [ ] Consul/Etcd 服务注册发现
- [ ] gRPC 服务框架
- [ ] JWT 认证中间件
- [ ] OAuth2 授权
- [ ] RBAC 权限管理
- [ ] API 网关
- [ ] 订单服务示例
- [ ] 分布式事务
- [ ] 服务限流熔断
- [ ] 单元测试和集成测试

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系项目维护者。
