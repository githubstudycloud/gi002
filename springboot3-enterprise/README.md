# Spring Boot 3.x 企业级多项目框架基座

基于 Spring Boot 3.2.5 构建的企业级多模块框架，集成了常用的企业级组件和最佳实践。

## 技术栈

- **JDK 17+** - Spring Boot 3.x 最低要求
- **Spring Boot 3.2.5** - 核心框架
- **MyBatis-Plus 3.5.5** - ORM框架
- **Sa-Token 1.37.0** - 权限认证
- **Redisson 3.27.2** - 分布式锁
- **Knife4j 4.4.0** - API文档
- **Hutool 5.8.26** - 工具包

## 项目结构

```
springboot3-enterprise/
├── enterprise-common     # 公共模块：工具类、异常、响应封装
├── enterprise-core       # 核心模块：安全、缓存、日志、AOP
├── enterprise-data       # 数据模块：MyBatis-Plus、Druid
├── enterprise-web        # Web模块：MVC、Swagger、全局异常
├── enterprise-mq         # 消息模块：RabbitMQ
├── enterprise-job        # 任务模块：Quartz、XXL-JOB
└── enterprise-demo       # 示例应用：端口 18080
```

## 中间件服务

已在远程服务器 (192.168.241.128) 部署以下服务：

| 服务 | 端口 | 说明 |
|------|------|------|
| MySQL | 13306 | 数据库 |
| Redis | 16379 | 缓存 |
| RabbitMQ | 15672 (AMQP) | 消息队列 |
| RabbitMQ | 15673 (管理) | 管理界面 |

### 连接信息

```yaml
# MySQL
host: 192.168.241.128
port: 13306
database: enterprise
username: root
password: Enterprise@2024

# Redis
host: 192.168.241.128
port: 16379
password: Enterprise@2024

# RabbitMQ
host: 192.168.241.128
port: 15672
username: admin
password: Enterprise@2024
vhost: /enterprise
```

## 快速开始

### 1. 构建项目

```bash
cd springboot3-enterprise
mvn clean install -DskipTests
```

### 2. 启动应用

```bash
cd enterprise-demo
mvn spring-boot:run
```

或使用环境变量连接本地/其他服务器：

```bash
mvn spring-boot:run -Dspring-boot.run.arguments="--MYSQL_HOST=localhost --REDIS_HOST=localhost"
```

### 3. 访问服务

- **API文档**: http://localhost:18080/doc.html
- **健康检查**: http://localhost:18080/test/health
- **Actuator**: http://localhost:18080/actuator
- **Druid监控**: http://localhost:18080/druid (admin/admin123)

## 核心功能

### 统一响应封装

```java
// 成功响应
Result.success(data);
Result.success("操作成功", data);

// 失败响应
Result.fail("操作失败");
Result.fail(ResultCode.PARAM_ERROR);
```

### 业务异常

```java
// 抛出业务异常
throw new BusinessException("用户不存在");
throw new BusinessException(ResultCode.DATA_NOT_FOUND, "用户不存在");

// 断言工具
AssertUtils.notNull(user, "用户不能为空");
AssertUtils.exists(data, "数据不存在");
```

### 缓存服务

```java
@Autowired
private CacheService cacheService;

// String操作
cacheService.set("key", value);
cacheService.setMinutes("key", value, 30);
String value = cacheService.get("key");

// Hash操作
cacheService.hSet("user", "name", "张三");
cacheService.hGetAll("user");
```

### 消息发送

```java
@Autowired
private MessageProducer messageProducer;

// 发送消息
BaseMessage message = BaseMessage.of("USER_REGISTER", userData);
messageProducer.sendDefault(message);
messageProducer.sendEmail(message);
```

### Sa-Token认证

```java
// 登录
StpUtil.login(userId);

// 获取当前用户
Long userId = StpUtil.getLoginIdAsLong();

// 权限校验
StpUtil.checkPermission("user:add");
StpUtil.checkRole("admin");
```

### MyBatis-Plus

```java
// 继承BaseEntity
@Data
@TableName("sys_user")
public class User extends BaseEntity {
    private String username;
}

// 分页查询
public IPage<User> page(PageQuery query) {
    return this.page(query.toPage());
}
```

## API示例

### 登录

```bash
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### 用户管理

```bash
# 分页查询
GET /api/users?pageNum=1&pageSize=10

# 创建用户
POST /api/users
{
  "username": "test",
  "password": "123456",
  "nickname": "测试用户"
}

# 更新用户
PUT /api/users/1
{
  "nickname": "新昵称"
}

# 删除用户
DELETE /api/users/1
```

### 测试接口

```bash
# 健康检查
GET /test/health

# 测试缓存
POST /test/cache?key=mykey&value=myvalue

# 测试消息
POST /test/message?type=TEST&content=hello

# 系统信息
GET /test/info
```

## 模块依赖说明

创建新的业务模块时，按需引入：

```xml
<!-- 基础Web应用 -->
<dependency>
    <groupId>com.enterprise</groupId>
    <artifactId>enterprise-web</artifactId>
</dependency>

<!-- 数据库访问 -->
<dependency>
    <groupId>com.enterprise</groupId>
    <artifactId>enterprise-data</artifactId>
</dependency>

<!-- 消息队列 -->
<dependency>
    <groupId>com.enterprise</groupId>
    <artifactId>enterprise-mq</artifactId>
</dependency>

<!-- 任务调度 -->
<dependency>
    <groupId>com.enterprise</groupId>
    <artifactId>enterprise-job</artifactId>
</dependency>
```

## 配置说明

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| MYSQL_HOST | localhost | MySQL主机 |
| MYSQL_PORT | 13306 | MySQL端口 |
| MYSQL_USER | root | MySQL用户名 |
| MYSQL_PASSWORD | Enterprise@2024 | MySQL密码 |
| REDIS_HOST | localhost | Redis主机 |
| REDIS_PORT | 16379 | Redis端口 |
| REDIS_PASSWORD | Enterprise@2024 | Redis密码 |
| RABBITMQ_HOST | localhost | RabbitMQ主机 |
| RABBITMQ_PORT | 15672 | RabbitMQ端口 |
| RABBITMQ_USER | admin | RabbitMQ用户 |
| RABBITMQ_PASSWORD | Enterprise@2024 | RabbitMQ密码 |

## 中间件管理

中间件部署在远程服务器 `/opt/enterprise-middleware` 目录：

```bash
# 启动服务
cd /opt/enterprise-middleware
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启单个服务
docker-compose restart mysql
```

## License

Apache 2.0
