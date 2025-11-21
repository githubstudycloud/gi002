# Python Enterprise Platform - 企业级多项目框架基座

## 项目概述

这是一个完整的Python企业级多项目框架基座，提供了构建微服务架构所需的所有核心组件。

## 架构设计

### 目录结构

```
python-enterprise-platform/
├── core-framework/          # 核心框架层
│   ├── database/           # 数据库抽象层 (SQLAlchemy, MongoDB, etc.)
│   ├── cache/              # 缓存抽象层 (Redis, Memcached)
│   ├── messaging/          # 消息队列抽象层 (RabbitMQ, Kafka)
│   ├── auth/               # 认证授权模块 (JWT, OAuth2, RBAC)
│   ├── logging/            # 统一日志系统
│   ├── config/             # 配置管理
│   ├── exceptions/         # 异常处理
│   └── middleware/         # 中间件集合
├── services/               # 微服务目录
│   ├── user-service/       # 用户服务示例
│   ├── order-service/      # 订单服务示例
│   └── gateway-service/    # API网关服务
├── shared-libs/            # 共享库
│   ├── common-utils/       # 通用工具类
│   ├── models/             # 共享数据模型
│   └── proto/              # gRPC Proto定义
├── infrastructure/         # 基础设施配置
│   ├── docker/             # Docker配置
│   ├── k8s/                # Kubernetes配置
│   └── mcp-servers/        # MCP服务器配置
├── tests/                  # 测试目录
│   ├── unit/               # 单元测试
│   ├── integration/        # 集成测试
│   └── e2e/                # 端到端测试
├── docs/                   # 文档目录
└── scripts/                # 脚本目录
```

## Python核心组件探究

### 1. Web框架
- **FastAPI**: 现代、快速的Web框架，基于类型提示
- **Flask**: 轻量级Web框架
- **Django**: 全栈Web框架

### 2. 数据库ORM
- **SQLAlchemy**: 最流行的Python ORM
- **Tortoise ORM**: 异步ORM
- **Peewee**: 轻量级ORM

### 3. 异步编程
- **asyncio**: Python标准库异步支持
- **aiohttp**: 异步HTTP客户端/服务器
- **uvloop**: 高性能事件循环

### 4. 消息队列
- **Celery**: 分布式任务队列
- **RQ**: 简单的任务队列
- **Kafka-Python**: Kafka客户端

### 5. 缓存
- **Redis**: 内存数据库和缓存
- **Memcached**: 分布式内存对象缓存

### 6. API文档
- **Swagger/OpenAPI**: API文档自动生成
- **ReDoc**: 美观的API文档

### 7. 测试框架
- **pytest**: 功能强大的测试框架
- **unittest**: Python标准库测试框架
- **coverage**: 代码覆盖率工具

### 8. 监控和日志
- **Prometheus**: 监控和报警
- **ELK Stack**: 日志收集和分析
- **structlog**: 结构化日志

## 技术栈

- **Python**: 3.11+
- **Web框架**: FastAPI, Flask
- **数据库**: PostgreSQL, MySQL, MongoDB
- **缓存**: Redis
- **消息队列**: RabbitMQ, Kafka
- **容器化**: Docker, Docker Compose
- **编排**: Kubernetes
- **监控**: Prometheus, Grafana
- **日志**: ELK Stack
- **API网关**: Kong, Traefik
- **服务发现**: Consul, Etcd

## MCP服务器集成

本项目支持通过MCP (Model Context Protocol) 连接各种中间件服务：

- PostgreSQL MCP Server
- Redis MCP Server
- MongoDB MCP Server
- RabbitMQ MCP Server
- Elasticsearch MCP Server

## 快速开始

### 1. 安装依赖

```bash
# 使用poetry管理依赖
poetry install

# 或使用pip
pip install -r requirements.txt
```

### 2. 启动基础设施

```bash
# 使用Docker Compose启动所有中间件
docker-compose up -d
```

### 3. 运行示例服务

```bash
# 启动用户服务
cd services/user-service
python main.py

# 启动订单服务
cd services/order-service
python main.py
```

## 开发指南

详见 [docs/development-guide.md](docs/development-guide.md)

## 部署指南

详见 [docs/deployment-guide.md](docs/deployment-guide.md)

## 许可证

MIT License
