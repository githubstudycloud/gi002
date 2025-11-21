# 系统架构文档

## 概述

Python企业级多项目框架是一个基于微服务架构的现代化应用平台，提供了完整的基础设施和核心组件。

## 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        API Gateway                           │
│                      (Kong / Traefik)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┬──────────────┐
         │                       │              │
┌────────▼────────┐   ┌─────────▼──────┐   ┌──▼─────────────┐
│  User Service   │   │  Order Service │   │  Other Services│
│   (FastAPI)     │   │   (FastAPI)    │   │                │
└────────┬────────┘   └────────┬───────┘   └──┬─────────────┘
         │                     │              │
         └──────────┬──────────┴──────────────┘
                    │
         ┌──────────┴───────────┐
         │                      │
┌────────▼────────┐   ┌────────▼────────┐
│  Core Framework │   │  Shared Libs    │
│                 │   │                 │
│  - Database     │   │  - Common Utils │
│  - Cache        │   │  - Models       │
│  - Messaging    │   │  - Proto        │
│  - Auth         │   │                 │
│  - Logging      │   │                 │
│  - Config       │   │                 │
└────────┬────────┘   └─────────────────┘
         │
         │
┌────────▼────────────────────────────────┐
│          Infrastructure                  │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │PostgreSQL│  │  Redis   │  │MongoDB ││
│  └──────────┘  └──────────┘  └────────┘│
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │RabbitMQ  │  │Elastic   │  │Prometheus│
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
```

## 核心组件

### 1. Core Framework (核心框架层)

核心框架层提供了可复用的基础组件，供所有微服务使用。

#### 1.1 Database (数据库抽象层)

**功能：**
- 统一的数据库访问接口
- 支持多种数据库：PostgreSQL, MySQL, MongoDB, SQLite
- 异步操作
- 连接池管理
- 事务支持

**关键类：**
- `DatabaseBase`: 数据库基类
- `SQLDatabase`: SQL数据库实现
- `MongoDBDatabase`: MongoDB实现

**使用示例：**
```python
from database import SQLDatabase, DatabaseConfig, DatabaseType

config = DatabaseConfig(
    type=DatabaseType.POSTGRESQL,
    host="localhost",
    port=5432,
    username="postgres",
    password="postgres",
    database="mydb"
)

db = SQLDatabase(config)
await db.connect()

# 查询
users = await db.fetch_all("SELECT * FROM users")

# 事务
async with db.transaction() as session:
    await session.execute("INSERT INTO users ...")
```

#### 1.2 Cache (缓存抽象层)

**功能：**
- 统一的缓存访问接口
- 支持多种缓存：Redis, Memcached, Memory
- 序列化/反序列化
- TTL管理
- LRU淘汰策略(内存缓存)

**关键类：**
- `CacheBase`: 缓存基类
- `RedisCache`: Redis实现
- `MemoryCache`: 内存缓存实现

**使用示例：**
```python
from cache import RedisCache, CacheConfig, CacheType

config = CacheConfig(
    type=CacheType.REDIS,
    host="localhost",
    port=6379
)

cache = RedisCache(config)
await cache.connect()

# 设置缓存
await cache.set("user:1", user_data, ttl=300)

# 获取缓存
user = await cache.get("user:1")

# Hash操作
await cache.hset("user:profile:1", "name", "John")
```

#### 1.3 Messaging (消息队列抽象层)

**功能：**
- 统一的消息队列接口
- 支持：RabbitMQ, Kafka, Redis Stream
- 发布/订阅模式
- 消息确认机制
- 消费者管理

**关键类：**
- `MessageQueueBase`: 消息队列基类
- `RabbitMQQueue`: RabbitMQ实现
- `RedisQueue`: Redis队列实现

**使用示例：**
```python
from messaging import RabbitMQQueue, MessageQueueConfig, Message

config = MessageQueueConfig(
    type=QueueType.RABBITMQ,
    host="localhost",
    port=5672
)

mq = RabbitMQQueue(config)
await mq.connect()

# 发布消息
message = Message(body={"user_id": 1, "action": "create"})
await mq.publish("user_events", message)

# 消费消息
async def handle_message(msg: Message):
    print(f"Received: {msg.body}")

await mq.consume("user_events", handle_message)
```

#### 1.4 Auth (认证授权)

**功能：**
- JWT令牌管理
- 密码加密/验证
- RBAC权限控制
- 角色管理

**关键类：**
- `JWTHandler`: JWT处理器
- `PasswordHandler`: 密码处理器
- `RBACManager`: RBAC管理器

**使用示例：**
```python
from auth import create_access_token, verify_password, RBACManager

# JWT
token = create_access_token({"sub": "user123"})

# 密码
hashed = hash_password("mypassword")
is_valid = verify_password("mypassword", hashed)

# RBAC
rbac = RBACManager()
has_perm = rbac.user_has_permission(
    user_roles=["user"],
    permission=Permission.USER_READ
)
```

#### 1.5 Logging (日志系统)

**功能：**
- 结构化日志
- 多级别日志
- 文件/控制台输出
- JSON格式支持
- 上下文绑定

**使用示例：**
```python
from logging import get_logger

logger = get_logger(__name__)

logger.info("User created", user_id=123, username="john")
logger.error("Database error", error=str(e), query=sql)

# 绑定上下文
bound_logger = logger.bind(request_id="abc123")
bound_logger.info("Processing request")
```

#### 1.6 Config (配置管理)

**功能：**
- 环境变量支持
- 配置文件支持
- 类型验证
- 分层配置
- 热重载(可选)

**使用示例：**
```python
from config import get_settings

settings = get_settings()

# 应用配置
print(settings.app.app_name)

# 数据库配置
print(settings.database.postgres_url)

# Redis配置
print(settings.redis.redis_host)
```

#### 1.7 Exceptions (异常处理)

**功能：**
- 统一异常定义
- 异常处理器
- 错误码管理
- HTTP状态码映射

**关键类：**
- `BaseException`: 基础异常
- `ValidationError`: 验证错误
- `AuthenticationError`: 认证错误
- `NotFoundError`: 资源不存在

### 2. Services (微服务层)

#### 2.1 User Service (用户服务)

**职责：**
- 用户注册/登录
- 用户信息管理
- 认证授权
- 角色管理

**API端点：**
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新令牌
- `POST /api/v1/users/` - 创建用户
- `GET /api/v1/users/{id}` - 获取用户信息
- `PUT /api/v1/users/{id}` - 更新用户信息
- `DELETE /api/v1/users/{id}` - 删除用户

**技术栈：**
- FastAPI
- SQLAlchemy (异步)
- Redis缓存
- JWT认证

#### 2.2 Order Service (订单服务)

**职责：**
- 订单创建
- 订单查询
- 订单状态管理
- 订单历史

### 3. Infrastructure (基础设施层)

#### 3.1 数据存储

- **PostgreSQL**: 主数据库，存储结构化数据
- **MongoDB**: 文档数据库，存储非结构化数据
- **Redis**: 缓存和会话存储

#### 3.2 消息中间件

- **RabbitMQ**: 可靠的消息队列
- **Kafka**: 高吞吐量事件流(可选)

#### 3.3 监控和日志

- **Prometheus**: 指标收集
- **Grafana**: 可视化面板
- **Elasticsearch**: 日志存储
- **Kibana**: 日志查询和可视化

#### 3.4 服务发现和配置

- **Consul**: 服务注册和发现(可选)
- **Etcd**: 配置中心(可选)

## 设计原则

### 1. 微服务架构

每个服务独立开发、部署和扩展，服务间通过API通信。

### 2. 领域驱动设计 (DDD)

按业务领域划分服务，清晰的边界和职责。

### 3. CQRS模式

命令和查询分离，提高系统性能和可扩展性。

### 4. 事件驱动架构

使用消息队列实现服务间异步通信和事件传播。

### 5. 十二要素应用

- 配置外部化
- 无状态进程
- 日志流
- 环境等价
- 等等

## 数据流

### 用户登录流程

```
1. 客户端 -> API Gateway -> User Service
2. User Service -> Database (验证用户)
3. User Service -> JWT Handler (生成令牌)
4. User Service -> Redis (缓存会话)
5. User Service -> 客户端 (返回令牌)
```

### 订单创建流程

```
1. 客户端 -> API Gateway -> Order Service
2. Order Service -> User Service (验证用户)
3. Order Service -> Database (创建订单)
4. Order Service -> Message Queue (发布订单事件)
5. Order Service -> 客户端 (返回订单信息)
6. Message Queue -> Notification Service (发送通知)
```

## 安全性

### 1. 认证
- JWT令牌
- 令牌刷新机制
- 令牌黑名单(可选)

### 2. 授权
- RBAC权限控制
- API级别权限检查
- 资源级别权限检查

### 3. 数据安全
- 密码加密(bcrypt)
- HTTPS通信
- 数据库连接加密
- 敏感数据脱敏

### 4. 防护
- 限流
- CORS配置
- SQL注入防护
- XSS防护

## 性能优化

### 1. 缓存策略
- 热点数据缓存
- 查询结果缓存
- 分布式缓存

### 2. 数据库优化
- 索引优化
- 查询优化
- 连接池管理
- 读写分离(可选)

### 3. 异步处理
- 异步I/O
- 后台任务队列
- 事件驱动

### 4. 负载均衡
- 服务水平扩展
- 负载均衡器
- 健康检查

## 可观测性

### 1. 日志
- 结构化日志
- 分级日志
- 集中式日志存储

### 2. 指标
- 业务指标
- 系统指标
- 自定义指标

### 3. 追踪
- 分布式追踪
- 请求链路追踪
- 性能分析

### 4. 告警
- 阈值告警
- 异常告警
- 自动恢复

## 部署架构

### 开发环境
- Docker Compose
- 本地数据库
- 热重载

### 测试环境
- Kubernetes
- 自动化测试
- CI/CD集成

### 生产环境
- Kubernetes集群
- 高可用配置
- 自动扩缩容
- 灾备方案
