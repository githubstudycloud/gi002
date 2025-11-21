# 部署文档

## 环境要求

### 开发环境
- JDK 1.8+
- Maven 3.6+
- MySQL 8.0+
- Redis 7.0+
- Docker (可选)

### 生产环境
- 4核8G内存以上
- CentOS 7.6+ / Ubuntu 20.04+
- Docker 20.10+
- Kubernetes 1.20+ (可选)

## 本地开发部署

### 1. 克隆项目

```bash
git clone https://github.com/your-org/springboot2-enterprise.git
cd springboot2-enterprise
```

### 2. 启动中间件

#### 方式一：使用 Docker Compose（推荐）

```bash
cd docker
docker-compose up -d

# 查看启动状态
docker-compose ps

# 查看日志
docker-compose logs -f mysql
docker-compose logs -f redis
docker-compose logs -f nacos
```

#### 方式二：手动安装

**MySQL 8.0**
```bash
# 安装 MySQL
sudo apt-get install mysql-server

# 导入数据库
mysql -uroot -p < sql/enterprise_system.sql
```

**Redis 7.0**
```bash
# 安装 Redis
sudo apt-get install redis-server

# 启动 Redis
sudo systemctl start redis
```

**Nacos 2.2.0**
```bash
# 下载 Nacos
wget https://github.com/alibaba/nacos/releases/download/2.2.0/nacos-server-2.2.0.tar.gz
tar -xvf nacos-server-2.2.0.tar.gz
cd nacos/bin

# 单机模式启动
sh startup.sh -m standalone
```

### 3. 编译项目

```bash
# 安装父 POM
mvn clean install -DskipTests

# 或者单独编译各模块
cd enterprise-common && mvn clean install -DskipTests
cd ../enterprise-gateway && mvn clean install -DskipTests
cd ../enterprise-auth && mvn clean install -DskipTests
cd ../enterprise-modules/system && mvn clean install -DskipTests
```

### 4. 启动服务

**方式一：使用 Maven 插件**

```bash
# 启动网关 (终端1)
cd enterprise-gateway
mvn spring-boot:run

# 启动认证服务 (终端2)
cd enterprise-auth
mvn spring-boot:run

# 启动系统服务 (终端3)
cd enterprise-modules/system
mvn spring-boot:run
```

**方式二：使用 JAR 包**

```bash
# 打包
mvn clean package -DskipTests

# 启动网关
java -jar enterprise-gateway/target/enterprise-gateway.jar

# 启动认证服务
java -jar enterprise-auth/target/enterprise-auth.jar

# 启动系统服务
java -jar enterprise-modules/system/target/enterprise-system.jar
```

### 5. 验证服务

```bash
# 检查 Nacos 注册
curl http://localhost:8848/nacos/v1/ns/instance/list?serviceName=enterprise-gateway

# 测试认证服务
curl -X POST http://localhost:9527/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 测试系统服务
curl http://localhost:9527/system/user/list
```

## 生产环境部署

### Docker 部署

#### 1. 构建镜像

```bash
# 构建所有服务的 Docker 镜像
mvn clean package docker:build

# 或单独构建
cd enterprise-gateway
mvn clean package docker:build
```

#### 2. 推送到镜像仓库

```bash
docker tag enterprise-gateway:1.0.0 your-registry.com/enterprise-gateway:1.0.0
docker push your-registry.com/enterprise-gateway:1.0.0
```

#### 3. 运行容器

```bash
# 创建网络
docker network create enterprise-net

# 运行网关
docker run -d \
  --name enterprise-gateway \
  --network enterprise-net \
  -p 9527:9527 \
  -e NACOS_ADDR=nacos:8848 \
  -e REDIS_HOST=redis \
  enterprise-gateway:1.0.0

# 运行认证服务
docker run -d \
  --name enterprise-auth \
  --network enterprise-net \
  -p 9200:9200 \
  -e NACOS_ADDR=nacos:8848 \
  -e REDIS_HOST=redis \
  enterprise-auth:1.0.0

# 运行系统服务
docker run -d \
  --name enterprise-system \
  --network enterprise-net \
  -p 9201:9201 \
  -e NACOS_ADDR=nacos:8848 \
  -e MYSQL_HOST=mysql \
  -e REDIS_HOST=redis \
  enterprise-system:1.0.0
```

### Kubernetes 部署

#### 1. 创建命名空间

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: enterprise
```

```bash
kubectl apply -f namespace.yaml
```

#### 2. 部署 ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: enterprise-config
  namespace: enterprise
data:
  nacos.addr: "nacos.enterprise.svc.cluster.local:8848"
  mysql.host: "mysql.enterprise.svc.cluster.local"
  redis.host: "redis.enterprise.svc.cluster.local"
```

#### 3. 部署服务

```yaml
# gateway-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: enterprise-gateway
  namespace: enterprise
spec:
  replicas: 2
  selector:
    matchLabels:
      app: enterprise-gateway
  template:
    metadata:
      labels:
        app: enterprise-gateway
    spec:
      containers:
      - name: gateway
        image: your-registry.com/enterprise-gateway:1.0.0
        ports:
        - containerPort: 9527
        env:
        - name: NACOS_ADDR
          valueFrom:
            configMapKeyRef:
              name: enterprise-config
              key: nacos.addr
---
apiVersion: v1
kind: Service
metadata:
  name: enterprise-gateway
  namespace: enterprise
spec:
  type: NodePort
  ports:
  - port: 9527
    targetPort: 9527
    nodePort: 30527
  selector:
    app: enterprise-gateway
```

```bash
kubectl apply -f gateway-deployment.yaml
```

## 远程服务器部署（使用 MCP）

### 通过 MCP 连接远程服务器

远程服务器已经配置了以下中间件：
- MySQL: 端口 13306
- Redis: 端口 16379
- RabbitMQ: 端口 15672/15673

### 修改配置连接远程服务

修改各服务的 `application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:mysql://remote-server-ip:13306/enterprise_system
  redis:
    host: remote-server-ip
    port: 16379
  cloud:
    nacos:
      discovery:
        server-addr: remote-server-ip:8848
```

## 性能优化

### JVM 参数调优

```bash
java -jar \
  -Xms2g -Xmx2g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/logs/heapdump.hprof \
  -Dspring.profiles.active=prod \
  enterprise-system.jar
```

### 连接池配置

```yaml
spring:
  datasource:
    druid:
      initial-size: 10
      min-idle: 10
      max-active: 50
      max-wait: 60000
  redis:
    lettuce:
      pool:
        max-active: 200
        max-idle: 50
        min-idle: 10
```

## 监控与日志

### 1. Actuator 监控

访问监控端点：
```
http://localhost:9201/actuator/health
http://localhost:9201/actuator/metrics
http://localhost:9201/actuator/info
```

### 2. 日志配置

```yaml
logging:
  file:
    name: /logs/enterprise-system.log
  level:
    root: INFO
    com.enterprise: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
```

### 3. ELK 日志收集

配置 Logstash 收集日志到 Elasticsearch：

```conf
input {
  file {
    path => "/logs/*.log"
    type => "enterprise-log"
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{DATA:thread}\] %{LOGLEVEL:level} %{DATA:logger} - %{GREEDYDATA:message}" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "enterprise-logs-%{+YYYY.MM.dd}"
  }
}
```

## 故障排查

### 服务启动失败

1. 检查日志文件
2. 确认中间件服务状态
3. 验证配置文件正确性
4. 检查端口占用

### 服务无法注册到 Nacos

1. 检查 Nacos 服务状态
2. 验证网络连通性
3. 确认配置地址正确

### 数据库连接失败

1. 检查 MySQL 服务状态
2. 验证用户名密码
3. 确认数据库已创建
4. 检查防火墙规则

## 安全建议

1. 修改默认密码
2. 启用 HTTPS
3. 配置防火墙规则
4. 定期备份数据
5. 监控异常访问

## 备份与恢复

### 数据库备份

```bash
# 备份
mysqldump -h127.0.0.1 -P3306 -uroot -proot enterprise_system > backup.sql

# 恢复
mysql -h127.0.0.1 -P3306 -uroot -proot enterprise_system < backup.sql
```

### Redis 备份

```bash
# 触发保存
redis-cli BGSAVE

# 拷贝 RDB 文件
cp /var/lib/redis/dump.rdb /backup/
```

---

**最后更新**: 2025-11-20
