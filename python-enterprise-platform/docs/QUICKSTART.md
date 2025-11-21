# 快速开始指南

本指南将帮助您快速搭建和运行Python企业级多项目框架。

## 环境要求

- Python 3.11+
- Docker 20.10+
- Docker Compose 2.0+
- Git

## 1. 克隆项目

```bash
git clone <repository-url>
cd python-enterprise-platform
```

## 2. 配置环境变量

复制环境变量模板并根据需要修改：

```bash
cp infrastructure/mcp-servers/.env.example .env
```

编辑 `.env` 文件，配置数据库、Redis等连接信息。

## 3. 启动基础设施

使用Docker Compose启动所有中间件服务：

```bash
docker-compose up -d postgres redis mongodb rabbitmq elasticsearch
```

等待所有服务启动完成(约1-2分钟)，可以使用以下命令查看状态：

```bash
docker-compose ps
```

## 4. 安装Python依赖

### 使用pip

```bash
pip install -r requirements.txt
```

### 使用poetry (推荐)

```bash
# 安装poetry
pip install poetry

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

## 5. 初始化数据库

创建数据库表：

```bash
cd services/user-service
python -c "
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent.parent / 'core-framework'))
from app.dependencies import get_database
from app.models.user import User

async def init_db():
    db = get_database()
    await db.connect()
    await db.create_tables()
    print('数据库表创建成功')
    await db.disconnect()

asyncio.run(init_db())
"
```

## 6. 启动用户服务

```bash
cd services/user-service
python main.py
```

服务将在 `http://localhost:8000` 启动。

## 7. 访问API文档

打开浏览器访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 8. 测试API

### 创建用户

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456!",
    "full_name": "Test User"
  }'
```

### 用户登录

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123456!"
  }'
```

返回的 `access_token` 用于后续的API调用。

### 获取用户信息

```bash
curl -X GET "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer <your-access-token>"
```

## 9. 访问监控面板

### RabbitMQ管理界面
- URL: http://localhost:15672
- 用户名: guest
- 密码: guest

### Kibana (Elasticsearch可视化)
- URL: http://localhost:5601

### Grafana (监控可视化)
- URL: http://localhost:3000
- 用户名: admin
- 密码: admin

### Prometheus
- URL: http://localhost:9090

## 10. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_database.py

# 生成覆盖率报告
pytest --cov=. --cov-report=html
```

## 11. 使用Docker启动完整服务

如果您想使用Docker启动整个应用(包括服务):

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f user-service

# 停止所有服务
docker-compose down
```

## 常见问题

### 1. 端口冲突

如果端口已被占用，修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "5433:5432"  # 修改为其他端口
```

### 2. 数据库连接失败

确保数据库服务已启动并健康：

```bash
docker-compose ps
docker-compose logs postgres
```

### 3. 依赖安装失败

尝试升级pip：

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 下一步

- 查看[开发指南](DEVELOPMENT.md)了解如何开发新功能
- 查看[部署指南](DEPLOYMENT.md)了解如何部署到生产环境
- 查看[架构文档](ARCHITECTURE.md)了解系统架构设计

## 获取帮助

- 查看项目README
- 提交Issue到GitHub仓库
- 查看API文档: http://localhost:8000/docs
