# 快速开始指南

本指南将帮助您在5分钟内启动并运行Spring Boot 4.x企业平台。

## 前置检查

确保您的环境满足以下要求:

```bash
# 检查Java版本 (需要21+)
java -version

# 检查Maven版本 (需要3.9+)
mvn -version

# 检查Docker版本
docker --version
docker-compose --version
```

## 三步启动

### 步骤 1: 启动中间件

**Windows:**
```cmd
cd springboot4-enterprise-platform\docker-compose
start-all.bat
```

**Linux/Mac:**
```bash
cd springboot4-enterprise-platform/docker-compose
chmod +x start-all.sh
./start-all.sh
```

等待约30秒,所有服务将启动完成。

### 步骤 2: 构建项目

```bash
cd springboot4-enterprise-platform
mvn clean install -DskipTests
```

首次构建可能需要5-10分钟下载依赖。

### 步骤 3: 启动用户服务

```bash
cd platform-services/service-user
mvn spring-boot:run
```

## 验证运行

### 1. 检查服务健康

```bash
curl http://localhost:8081/actuator/health
```

期望响应:
```json
{
  "status": "UP"
}
```

### 2. 检查中间件连接

访问以下URL验证各服务:

- **RabbitMQ管理界面**: http://localhost:15672 (admin/password)
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### 3. 查看指标

```bash
curl http://localhost:8081/actuator/metrics
curl http://localhost:8081/actuator/prometheus
```

## 下一步

### 探索Spring Boot 4.x新特性

查看 [SPRINGBOOT4_FEATURES.md](SPRINGBOOT4_FEATURES.md) 了解:

- 内置弹性机制 (@Retryable, @ConcurrencyLimit)
- API版本控制
- JSpecify空安全
- 虚拟线程支持

### 开发您的服务

1. **创建实体类**

```java
@Entity
@Table(name = "users")
@Data
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;
    private String email;
}
```

2. **创建Repository**

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}
```

3. **创建Service**

```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    @Retryable(maxAttempts = 3)  // Spring Framework 7新特性
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new BusinessException("User not found"));
    }
}
```

4. **创建Controller**

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{id}")
    public Result<User> getUser(@PathVariable Long id) {
        return Result.success(userService.findById(id));
    }
}
```

### 配置其他服务

复制 `service-user` 模块创建新服务:

```bash
cp -r platform-services/service-user platform-services/service-xxx
```

修改:
1. `pom.xml` 中的 `artifactId`
2. 主类名和包名
3. `application.yml` 中的端口号

### 使用Docker Compose测试

所有中间件服务都在Docker中运行:

```bash
# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f [service-name]

# 重启服务
docker-compose restart [service-name]

# 停止所有服务
docker-compose down
```

## 常用命令

### 项目构建

```bash
# 完整构建
mvn clean install

# 跳过测试
mvn clean install -DskipTests

# 只构建特定模块
mvn clean install -pl platform-services/service-user -am
```

### 运行服务

```bash
# 开发模式运行
mvn spring-boot:run

# 使用特定配置文件
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# 调试模式
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"
```

### Docker操作

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose stop

# 查看日志
docker-compose logs -f

# 重建并启动
docker-compose up -d --build

# 清理所有容器和数据
docker-compose down -v
```

## 故障排查

### 端口被占用

**Windows:**
```cmd
netstat -ano | findstr :8081
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8081 | xargs kill -9
```

### Maven构建失败

```bash
# 清理本地仓库缓存
mvn dependency:purge-local-repository

# 强制更新
mvn clean install -U
```

### Docker服务无法启动

```bash
# 查看详细日志
docker-compose logs [service-name]

# 重建容器
docker-compose up -d --force-recreate [service-name]

# 完全重置
docker-compose down -v
docker system prune -a
docker-compose up -d
```

### 数据库连接失败

1. 检查Docker容器是否运行: `docker-compose ps`
2. 检查端口是否开放: `telnet localhost 3306`
3. 查看容器日志: `docker-compose logs mysql`
4. 重启容器: `docker-compose restart mysql`

## 性能调优

### JVM参数

```bash
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xms512m -Xmx2048m -XX:+UseG1GC"
```

### 启用虚拟线程

```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true
```

### 数据库连接池

```yaml
spring:
  datasource:
    hikari:
      minimum-idle: 5
      maximum-pool-size: 20
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
```

## 生产部署

### 构建可执行JAR

```bash
mvn clean package -DskipTests
java -jar platform-services/service-user/target/service-user-1.0.0-SNAPSHOT.jar
```

### 构建Docker镜像

```bash
cd platform-services/service-user
mvn spring-boot:build-image
docker run -p 8081:8081 service-user:1.0.0-SNAPSHOT
```

### 构建原生镜像 (GraalVM)

```bash
mvn -Pnative spring-boot:build-image
```

启动时间从2秒降至0.05秒!

## 获取帮助

- 📖 查看完整文档: [README.md](README.md)
- 🚀 学习新特性: [SPRINGBOOT4_FEATURES.md](SPRINGBOOT4_FEATURES.md)
- 🔧 测试中间件: [MCP_TESTING_GUIDE.md](MCP_TESTING_GUIDE.md)
- 🐛 问题反馈: [GitHub Issues]

## 项目结构速览

```
springboot4-enterprise-platform/
├── platform-common/           # 通用模块
│   ├── common-core/          # 工具类、常量
│   ├── common-domain/        # 领域模型
│   └── common-exception/     # 异常处理
├── platform-framework/       # 框架层
│   ├── framework-security/   # 安全认证
│   ├── framework-data/       # 数据访问
│   ├── framework-cache/      # 缓存
│   ├── framework-mq/         # 消息队列
│   └── framework-observability/ # 可观测性
├── platform-services/        # 业务服务
│   ├── service-user/         # 用户服务 ✓
│   ├── service-order/        # 订单服务
│   └── service-product/      # 产品服务
└── docker-compose/           # 中间件编排
```

## 技术栈一览

| 分类 | 技术 | 版本 |
|------|------|------|
| 核心 | Java | 21 |
| 框架 | Spring Boot | 4.0.0-M2 |
| 数据库 | MySQL | 9.1 |
| 缓存 | Redis | 7.4 |
| 消息 | RabbitMQ | 4.0 |
| 流处理 | Kafka | 3.9 |
| 监控 | Prometheus | Latest |
| 可视化 | Grafana | Latest |

## 开始您的开发之旅

```bash
# 1. 克隆项目 (如果从Git)
git clone <repository-url>

# 2. 启动中间件
cd docker-compose && ./start-all.sh

# 3. 构建项目
cd .. && mvn clean install

# 4. 运行服务
cd platform-services/service-user && mvn spring-boot:run

# 5. 开始编码! 🚀
```

祝您开发愉快! 🎉
