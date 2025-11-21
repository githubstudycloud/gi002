# Spring Boot 2.x 企业级多项目框架基座

## 项目简介

这是一个基于 Spring Boot 2.7.x 和 Spring Cloud 2021.x 构建的企业级微服务框架基座，集成了主流的微服务组件和中间件，提供了完整的企业级应用开发解决方案。

## 技术栈

### 核心框架
- **Spring Boot**: 2.7.18
- **Spring Cloud**: 2021.0.8
- **Spring Cloud Alibaba**: 2021.0.5.0
- **JDK**: 1.8+

### 数据层
- **MyBatis Plus**: 3.5.5
- **MySQL**: 8.0+
- **Druid**: 1.2.20
- **Redis**: 7.0+

### 微服务组件
- **Nacos**: 服务注册与配置中心
- **Spring Cloud Gateway**: API网关
- **Spring Security + JWT**: 安全认证
- **Seata**: 分布式事务
- **RabbitMQ**: 消息队列

### 工具类
- **Hutool**: 5.8.24
- **FastJson2**: 2.0.43
- **Lombok**: 1.18.30
- **Knife4j**: API文档

## 项目结构

```
springboot2-enterprise/
├── enterprise-common/              # 公共模块
│   ├── common-core/               # 核心工具类
│   ├── common-redis/              # Redis配置
│   ├── common-log/                # 日志模块
│   ├── common-security/           # 安全模块
│   ├── common-swagger/            # API文档
│   └── common-mybatis/            # MyBatis配置
├── enterprise-gateway/            # 网关服务 (9527)
├── enterprise-auth/               # 认证服务 (9200)
├── enterprise-modules/            # 业务模块
│   ├── system/                   # 系统管理 (9201)
│   ├── generator/                # 代码生成
│   └── job/                      # 定时任务
├── sql/                          # 数据库脚本
├── docker/                       # Docker配置
└── docs/                         # 项目文档
```

## 服务端口规划

| 服务名称 | 端口 | 说明 |
|---------|------|------|
| enterprise-gateway | 9527 | API网关 |
| enterprise-auth | 9200 | 认证授权服务 |
| enterprise-system | 9201 | 系统管理服务 |
| Nacos | 8848 | 服务注册中心 |
| MySQL | 3306 | 数据库 |
| Redis | 6379 | 缓存 |
| RabbitMQ | 5672/15672 | 消息队列 |

## 快速开始

### 1. 环境准备

确保本地已安装：
- JDK 1.8+
- Maven 3.6+
- Docker & Docker Compose

### 2. 启动中间件

使用 Docker Compose 快速启动所有中间件：

```bash
cd docker
docker-compose up -d
```

这将启动以下服务：
- MySQL 8.0
- Redis 7.0
- Nacos 2.2.0
- RabbitMQ 3.12
- Elasticsearch 7.17
- Kibana 7.17
- Seata Server 1.7.1

### 3. 初始化数据库

执行数据库初始化脚本：

```bash
mysql -h127.0.0.1 -P3306 -uroot -proot < sql/enterprise_system.sql
```

### 4. 编译项目

```bash
mvn clean install -DskipTests
```

### 5. 启动服务

按以下顺序启动服务：

**1) 启动网关服务**
```bash
cd enterprise-gateway
mvn spring-boot:run
```

**2) 启动认证服务**
```bash
cd enterprise-auth
mvn spring-boot:run
```

**3) 启动系统管理服务**
```bash
cd enterprise-modules/system
mvn spring-boot:run
```

### 6. 访问服务

- **Nacos控制台**: http://localhost:8848/nacos (用户名/密码: nacos/nacos)
- **Druid监控**: http://localhost:9201/druid (用户名/密码: admin/admin)
- **RabbitMQ管理**: http://localhost:15672 (用户名/密码: admin/admin123)
- **Kibana**: http://localhost:5601

## 核心功能

### 1. 统一响应封装

使用 `R<T>` 统一响应结果：

```java
@GetMapping("/list")
public R<List<SysUser>> list() {
    List<SysUser> users = userService.list();
    return R.ok(users);
}
```

### 2. 全局异常处理

自动捕获并处理各类异常：

```java
@ExceptionHandler(BaseException.class)
public R<?> handleBaseException(BaseException e) {
    return R.fail(e.getCode(), e.getMessage());
}
```

### 3. Redis缓存服务

提供便捷的缓存操作：

```java
@Autowired
private RedisService redisService;

// 设置缓存
redisService.set("key", value, 30, TimeUnit.MINUTES);

// 获取缓存
String value = redisService.get("key");
```

### 4. MyBatis Plus 集成

简化数据库操作：

```java
@Mapper
public interface SysUserMapper extends BaseMapper<SysUser> {
}

// 使用
List<SysUser> users = userMapper.selectList(null);
```

### 5. JWT 认证

基于 JWT 的无状态认证：

```java
POST /auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

## 开发指南

### 新增业务模块

1. 在 `enterprise-modules` 下创建新模块
2. 在模块的 `pom.xml` 中引入所需依赖
3. 创建启动类并标注 `@SpringBootApplication`
4. 配置 `application.yml`
5. 在父 POM 中添加模块引用

### 配置文件说明

**application.yml 主要配置：**

```yaml
spring:
  application:
    name: service-name
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
  datasource:
    url: jdbc:mysql://localhost:3306/database
    username: root
    password: root
  redis:
    host: 127.0.0.1
    port: 6379
```

## 部署说明

### Docker 部署

每个服务都配置了 Docker 构建插件，可以打包成 Docker 镜像：

```bash
# 构建镜像
mvn clean package docker:build

# 运行容器
docker run -d -p 9201:9201 enterprise-system:1.0.0
```

### Kubernetes 部署

提供完整的 K8s 部署配置文件（待完善）。

## 监控与运维

### 服务健康检查

所有服务都提供健康检查端点：

```
GET /actuator/health
```

### 日志收集

集成 ELK 日志收集系统：
- Elasticsearch: 存储日志
- Logstash: 收集日志
- Kibana: 可视化分析

## 常见问题

**Q: Nacos 启动失败？**
A: 检查 MySQL 是否已启动，Nacos 需要依赖 MySQL。

**Q: 服务无法注册到 Nacos？**
A: 检查 Nacos 地址配置是否正确，确保网络连通。

**Q: Redis 连接失败？**
A: 检查 Redis 服务状态和连接配置。

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 开源协议

MIT License

## 联系方式

如有问题，请通过以下方式联系：
- Issue: https://github.com/your-org/springboot2-enterprise/issues
- Email: support@enterprise.com

---

**最后更新**: 2025-11-20
