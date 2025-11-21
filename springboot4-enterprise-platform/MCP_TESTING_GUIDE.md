# MCP服务连接测试指南

本指南详细说明如何通过Docker Compose启动所有中间件服务,并测试它们的连接。

## 前提条件

- Docker Desktop 已安装并运行
- Docker Compose 已安装
- 端口 3000, 3306, 5432, 5672, 6379, 9090, 9092, 15672 未被占用

## 快速启动

### Windows系统

```cmd
cd docker-compose
start-all.bat
```

### Linux/Mac系统

```bash
cd docker-compose
chmod +x start-all.sh
./start-all.sh
```

## 手动启动步骤

### 1. 启动所有服务

```bash
cd docker-compose
docker-compose up -d
```

### 2. 查看服务状态

```bash
docker-compose ps
```

期望输出:
```
NAME                    STATUS      PORTS
enterprise-mysql        Up          0.0.0.0:3306->3306/tcp
enterprise-postgres     Up          0.0.0.0:5432->5432/tcp
enterprise-redis        Up          0.0.0.0:6379->6379/tcp
enterprise-rabbitmq     Up          0.0.0.0:5672->5672/tcp, 0.0.0.0:15672->15672/tcp
enterprise-kafka        Up          0.0.0.0:9092->9092/tcp
enterprise-prometheus   Up          0.0.0.0:9090->9090/tcp
enterprise-grafana      Up          0.0.0.0:3000->3000/tcp
```

## 连接测试

### MySQL测试

#### 通过Docker命令

```bash
# 测试连接
docker exec -it enterprise-mysql mysql -uroot -ppassword

# 查看数据库
mysql> SHOW DATABASES;
mysql> USE user_db;
mysql> SHOW TABLES;
```

#### 通过应用程序

```java
// application.yml配置
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/user_db
    username: root
    password: password
```

#### 使用MySQL客户端工具

- Host: localhost
- Port: 3306
- User: root
- Password: password
- Database: user_db

### PostgreSQL测试

#### 通过Docker命令

```bash
# 测试连接
docker exec -it enterprise-postgres psql -U postgres

# 查看数据库
postgres=# \l
postgres=# \c user_db
postgres=# \dt
```

#### 通过应用程序

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/user_db
    username: postgres
    password: password
```

#### 使用pgAdmin或DBeaver

- Host: localhost
- Port: 5432
- User: postgres
- Password: password
- Database: user_db

### Redis测试

#### 通过Docker命令

```bash
# 连接Redis CLI
docker exec -it enterprise-redis redis-cli

# 测试基本操作
127.0.0.1:6379> PING
PONG
127.0.0.1:6379> SET test "Hello World"
OK
127.0.0.1:6379> GET test
"Hello World"
127.0.0.1:6379> DEL test
```

#### 通过应用程序

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
```

#### 使用Redis Desktop Manager

- Host: localhost
- Port: 6379
- Auth: (留空)

### RabbitMQ测试

#### 管理界面

访问: http://localhost:15672

- Username: admin
- Password: password

#### 通过Docker命令

```bash
# 查看状态
docker exec enterprise-rabbitmq rabbitmqctl status

# 列出队列
docker exec enterprise-rabbitmq rabbitmqctl list_queues

# 列出交换器
docker exec enterprise-rabbitmq rabbitmqctl list_exchanges
```

#### 通过应用程序

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: admin
    password: password
```

#### 创建测试队列

```bash
# 进入容器
docker exec -it enterprise-rabbitmq bash

# 创建队列
rabbitmqadmin declare queue name=test-queue durable=true

# 发布消息
rabbitmqadmin publish routing_key=test-queue payload="Hello RabbitMQ"

# 获取消息
rabbitmqadmin get queue=test-queue
```

### Kafka测试

#### 通过Docker命令

```bash
# 列出主题
docker exec enterprise-kafka kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092

# 创建主题
docker exec enterprise-kafka kafka-topics.sh \
  --create \
  --topic test-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# 生产消息
docker exec -it enterprise-kafka kafka-console-producer.sh \
  --topic test-topic \
  --bootstrap-server localhost:9092

# 消费消息
docker exec -it enterprise-kafka kafka-console-consumer.sh \
  --topic test-topic \
  --from-beginning \
  --bootstrap-server localhost:9092
```

#### 通过应用程序

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: user-service-group
      auto-offset-reset: earliest
```

### Prometheus测试

#### Web界面

访问: http://localhost:9090

#### 测试查询

在Prometheus UI中执行查询:

```promql
# 查看所有指标
{job="user-service"}

# 查看JVM内存使用
jvm_memory_used_bytes{job="user-service"}

# 查看HTTP请求
http_server_requests_seconds_count{job="user-service"}
```

#### 检查目标状态

访问: http://localhost:9090/targets

应该看到配置的服务目标(如果服务已启动)

### Grafana测试

#### Web界面

访问: http://localhost:3000

- Username: admin
- Password: admin

#### 配置Prometheus数据源

1. 左侧菜单: Configuration → Data Sources
2. 点击 "Add data source"
3. 选择 "Prometheus"
4. URL: http://prometheus:9090
5. 点击 "Save & Test"

#### 导入仪表板

1. 左侧菜单: Dashboards → Import
2. 输入仪表板ID: 4701 (JVM Micrometer)
3. 选择Prometheus数据源
4. 点击 Import

## 自动化测试脚本

### 运行连接测试

#### Linux/Mac

```bash
cd docker-compose
chmod +x test-connections.sh
./test-connections.sh
```

#### Windows

需要安装Git Bash或WSL,然后运行:

```bash
cd docker-compose
bash test-connections.sh
```

### 测试脚本功能

该脚本会自动测试:

1. ✓ MySQL连接和数据库存在性
2. ✓ PostgreSQL连接和数据库存在性
3. ✓ Redis PING/PONG测试
4. ✓ Redis读写测试
5. ✓ RabbitMQ状态检查
6. ✓ Kafka Broker连接
7. ✓ Kafka主题创建和列表
8. ✓ Prometheus健康检查
9. ✓ Grafana健康检查

## 常见问题排查

### 服务启动失败

```bash
# 查看服务日志
docker-compose logs [service-name]

# 例如:
docker-compose logs mysql
docker-compose logs redis
```

### 端口冲突

```bash
# 检查端口占用 (Windows)
netstat -ano | findstr :3306

# 检查端口占用 (Linux/Mac)
lsof -i :3306
```

### 重启服务

```bash
# 重启单个服务
docker-compose restart mysql

# 重启所有服务
docker-compose restart
```

### 完全重建

```bash
# 停止并删除所有容器、网络、卷
docker-compose down -v

# 重新启动
docker-compose up -d
```

### 清理Docker资源

```bash
# 清理未使用的容器、网络、镜像
docker system prune -a

# 清理卷(谨慎使用,会删除数据)
docker volume prune
```

## Spring Boot应用连接测试

### 1. 启动用户服务

```bash
cd platform-services/service-user
mvn spring-boot:run
```

### 2. 检查Actuator端点

```bash
# 健康检查
curl http://localhost:8081/actuator/health

# 查看指标
curl http://localhost:8081/actuator/metrics

# Prometheus格式指标
curl http://localhost:8081/actuator/prometheus
```

### 3. 测试数据库连接

查看应用日志,应该看到:

```
HikariPool-1 - Start completed.
Initialized JPA EntityManagerFactory
```

### 4. 测试Redis连接

在应用日志中查找:

```
Lettuce initialized
RedisConnectionFactory created
```

## 性能监控

### 查看资源使用

```bash
# 查看容器资源使用情况
docker stats

# 查看特定容器
docker stats enterprise-mysql enterprise-redis
```

### 预期资源占用

| 服务 | 内存 | CPU |
|------|------|-----|
| MySQL | ~400MB | 1-5% |
| PostgreSQL | ~200MB | 1-5% |
| Redis | ~50MB | 1-3% |
| RabbitMQ | ~150MB | 1-5% |
| Kafka | ~500MB | 2-10% |
| Prometheus | ~200MB | 1-5% |
| Grafana | ~100MB | 1-3% |

## 数据持久化

所有数据都存储在Docker volumes中:

```bash
# 查看volumes
docker volume ls | grep enterprise

# 备份MySQL数据
docker exec enterprise-mysql mysqldump -uroot -ppassword user_db > backup.sql

# 恢复MySQL数据
docker exec -i enterprise-mysql mysql -uroot -ppassword user_db < backup.sql
```

## 网络配置

所有服务运行在同一个Docker网络中:

```bash
# 查看网络
docker network inspect docker-compose_enterprise-network

# 服务间可以通过服务名互相访问
# 例如: mysql:3306, redis:6379
```

## 停止服务

```bash
# 停止所有服务(保留数据)
docker-compose stop

# 停止并删除容器(保留数据卷)
docker-compose down

# 停止并删除所有内容(包括数据)
docker-compose down -v
```

## 总结

按照本指南,您应该能够:

1. ✓ 成功启动所有中间件服务
2. ✓ 测试每个服务的连接
3. ✓ 配置Spring Boot应用连接
4. ✓ 监控服务健康状态
5. ✓ 排查常见问题

如有问题,请检查Docker日志和应用日志。
