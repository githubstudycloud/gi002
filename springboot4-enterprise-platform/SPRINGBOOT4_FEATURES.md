# Spring Boot 4.x & Spring Framework 7 新特性指南

本文档详细介绍了Spring Boot 4.x和Spring Framework 7的新特性及其在本项目中的应用。

## 目录

1. [内置弹性机制](#内置弹性机制)
2. [API版本控制](#api版本控制)
3. [JSpecify空安全](#jspecify空安全)
4. [虚拟线程支持](#虚拟线程支持)
5. [Jackson 3.x](#jackson-3x)
6. [测试改进](#测试改进)
7. [原生镜像支持](#原生镜像支持)

---

## 内置弹性机制

Spring Framework 7引入了内置的弹性机制,无需额外依赖即可实现重试和并发控制。

### @Retryable - 自动重试

自动重试失败的方法调用,支持配置重试次数、延迟和退避策略。

#### 基础用法

```java
import org.springframework.retry.annotation.Retryable;
import org.springframework.retry.annotation.Backoff;

@Service
public class ExternalApiService {

    /**
     * 基本重试:最多3次尝试
     */
    @Retryable(maxAttempts = 3)
    public String callExternalApi() {
        // 可能失败的外部API调用
        return restTemplate.getForObject("https://api.example.com/data", String.class);
    }

    /**
     * 带退避策略的重试:指数退避
     */
    @Retryable(
        maxAttempts = 5,
        backoff = @Backoff(
            delay = 1000,        // 初始延迟1秒
            multiplier = 2.0,    // 指数倍数
            maxDelay = 10000     // 最大延迟10秒
        )
    )
    public Data fetchData(String id) {
        return externalClient.getData(id);
    }

    /**
     * 指定可重试的异常类型
     */
    @Retryable(
        retryFor = {IOException.class, TimeoutException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 2000)
    )
    public void uploadFile(File file) throws IOException {
        ftpClient.upload(file);
    }
}
```

#### 带恢复方法

```java
@Service
public class PaymentService {

    @Retryable(
        maxAttempts = 3,
        backoff = @Backoff(delay = 1000),
        recover = "recoverPayment"
    )
    public PaymentResult processPayment(Order order) {
        // 调用支付网关
        return paymentGateway.charge(order.getAmount());
    }

    /**
     * 恢复方法:所有重试失败后调用
     */
    public PaymentResult recoverPayment(Exception e, Order order) {
        log.error("Payment failed after retries for order: {}", order.getId(), e);
        // 发送通知、记录日志等
        return PaymentResult.failed("Payment service unavailable");
    }
}
```

#### 响应式支持

```java
@Service
public class ReactiveService {

    /**
     * 支持响应式返回类型
     */
    @Retryable(maxAttempts = 3)
    public Mono<User> getUserAsync(Long id) {
        return webClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(User.class);
    }

    @Retryable(maxAttempts = 3)
    public Flux<Product> getProductsAsync() {
        return webClient.get()
            .uri("/products")
            .retrieve()
            .bodyToFlux(Product.class);
    }
}
```

### @ConcurrencyLimit - 并发限制

限制方法的并发执行数量,保护资源不被过载。

#### 基础用法

```java
import org.springframework.concurrent.ConcurrencyLimit;

@Service
public class ResourceIntensiveService {

    /**
     * 最多允许10个并发调用
     */
    @ConcurrencyLimit(10)
    public Report generateReport(ReportRequest request) {
        // 资源密集型操作
        return reportGenerator.generate(request);
    }

    /**
     * 限制数据库批处理并发
     */
    @ConcurrencyLimit(5)
    public void processBatch(List<Item> items) {
        items.forEach(item -> {
            // 处理每个项目
            processItem(item);
        });
    }

    /**
     * 超出限制时的行为控制
     */
    @ConcurrencyLimit(
        value = 20,
        waitTime = 5000  // 等待5秒,如果还是满则抛出异常
    )
    public void processOrder(Order order) {
        orderProcessor.process(order);
    }
}
```

#### 实际应用场景

```java
@Service
@RequiredArgsConstructor
public class ImageProcessingService {

    private final ImageProcessor imageProcessor;

    /**
     * 图片处理通常是CPU密集型操作
     * 限制并发数避免系统过载
     */
    @ConcurrencyLimit(value = 8, waitTime = 10000)
    @Retryable(maxAttempts = 2)
    public ProcessedImage processImage(InputStream imageStream) {
        return imageProcessor.resize(imageStream, 800, 600);
    }

    /**
     * 结合重试和并发限制
     * 批量处理时既要控制并发,又要处理失败
     */
    @ConcurrencyLimit(10)
    @Retryable(
        maxAttempts = 3,
        backoff = @Backoff(delay = 2000),
        recover = "recoverBatchProcessing"
    )
    public void processBatch(List<Image> images) {
        images.forEach(this::processImage);
    }

    public void recoverBatchProcessing(Exception e, List<Image> images) {
        log.error("Batch processing failed", e);
        // 将失败的批次存入队列稍后重试
        failedBatchQueue.add(images);
    }
}
```

---

## API版本控制

Spring Framework 7原生支持API版本控制,可以在同一个应用中维护多个API版本。

### 基于路径的版本控制

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    /**
     * V1 API - 返回基础用户信息
     */
    @GetMapping(value = "/{id}", version = "v1")
    public Result<UserV1DTO> getUserV1(@PathVariable Long id) {
        User user = userService.findById(id);
        return Result.success(UserV1DTO.from(user));
    }

    /**
     * V2 API - 返回增强的用户信息(包含统计数据)
     */
    @GetMapping(value = "/{id}", version = "v2")
    public Result<UserV2DTO> getUserV2(@PathVariable Long id) {
        User user = userService.findById(id);
        UserStats stats = userService.getUserStats(id);
        return Result.success(UserV2DTO.from(user, stats));
    }

    /**
     * V3 API - 异步响应式API
     */
    @GetMapping(value = "/{id}", version = "v3")
    public Mono<Result<UserV3DTO>> getUserV3(@PathVariable Long id) {
        return userService.findByIdAsync(id)
            .map(user -> Result.success(UserV3DTO.from(user)));
    }
}
```

### 基于Header的版本控制

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    /**
     * 通过Header指定版本: X-API-Version: v1
     */
    @GetMapping(
        value = "/{id}",
        version = "v1",
        versionType = VersionType.HEADER,
        versionHeader = "X-API-Version"
    )
    public Result<ProductDTO> getProductV1(@PathVariable Long id) {
        return Result.success(productService.getProductV1(id));
    }

    @GetMapping(
        value = "/{id}",
        version = "v2",
        versionType = VersionType.HEADER,
        versionHeader = "X-API-Version"
    )
    public Result<ProductDetailDTO> getProductV2(@PathVariable Long id) {
        return Result.success(productService.getProductV2(id));
    }
}
```

### 版本弃用通知

```java
@RestController
public class OrderController {

    /**
     * 标记为已弃用的API版本
     */
    @GetMapping(value = "/api/orders/{id}", version = "v1")
    @Deprecated(since = "2.0", forRemoval = true)
    @ApiResponse(
        responseCode = "299",
        description = "Deprecated - Use v2 API instead"
    )
    public Result<OrderDTO> getOrderV1(@PathVariable Long id) {
        // 在响应中添加弃用警告
        HttpHeaders headers = new HttpHeaders();
        headers.add("Warning", "299 - \"Deprecated API. Please migrate to v2\"");

        return Result.success(orderService.getOrder(id));
    }
}
```

---

## JSpecify空安全

Spring Framework 7迁移到JSpecify注解,提供更精确的空值契约。

### 基础用法

```java
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;

@Service
public class UserService {

    /**
     * 方法可能返回null
     */
    @Nullable
    public User findByUsername(String username) {
        return userRepository.findByUsername(username)
            .orElse(null);
    }

    /**
     * 方法保证不返回null
     */
    @NonNull
    public User getById(@NonNull Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new BusinessException("User not found"));
    }

    /**
     * 参数不能为null
     */
    public void updateUser(@NonNull User user) {
        validateUser(user);
        userRepository.save(user);
    }

    /**
     * 参数可以为null
     */
    public List<User> search(@Nullable String keyword) {
        if (keyword == null || keyword.isBlank()) {
            return userRepository.findAll();
        }
        return userRepository.findByKeyword(keyword);
    }
}
```

### 集合和泛型

```java
import org.jspecify.annotations.Nullable;

public class DataService<T> {

    /**
     * 返回的List不为null,但元素可能为null
     */
    public List<@Nullable T> findAll() {
        // 返回的列表本身不为null,但可能包含null元素
        return repository.findAllWithNulls();
    }

    /**
     * 返回的Map不为null,键不为null,值可能为null
     */
    public Map<String, @Nullable T> findMap() {
        return repository.findAsMap();
    }

    /**
     * 完全非空的集合
     */
    public List<T> findAllNonNull() {
        return repository.findAll().stream()
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
    }
}
```

### Kotlin互操作

```kotlin
// Kotlin代码可以正确理解JSpecify注解

class UserClient(private val userService: UserService) {

    fun getUser(id: Long): User {
        // getById标记为@NonNull,Kotlin知道返回非空
        return userService.getById(id)
    }

    fun findUser(username: String): User? {
        // findByUsername标记为@Nullable,Kotlin知道可能为null
        return userService.findByUsername(username)
    }
}
```

---

## 虚拟线程支持

Spring Boot 4.x充分支持Java 21的虚拟线程(Project Loom)。

### 启用虚拟线程

```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true  # 启用虚拟线程
```

### 异步处理

```java
@Configuration
@EnableAsync
public class AsyncConfig {

    /**
     * 使用虚拟线程的任务执行器
     */
    @Bean
    public TaskExecutor taskExecutor() {
        return new SimpleAsyncTaskExecutor("virtual-");
    }
}

@Service
public class AsyncService {

    @Async
    public CompletableFuture<String> processAsync(String data) {
        // 这个方法将在虚拟线程中执行
        return CompletableFuture.completedFuture(
            heavyComputation(data)
        );
    }
}
```

### Web请求处理

```java
@RestController
public class VirtualThreadController {

    /**
     * 每个请求在虚拟线程中处理
     * 可以支持数百万并发连接
     */
    @GetMapping("/long-running")
    public Result<String> longRunningTask() {
        // 即使这里阻塞,也不会耗尽线程池
        Thread.sleep(5000);
        return Result.success("Completed");
    }
}
```

---

## Jackson 3.x

Spring Boot 4.x使用Jackson 3.x,带来更好的性能和新特性。

### 时间处理

```java
@Data
public class EventDTO {

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime eventTime;

    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate eventDate;

    // Jackson 3.x更好地支持Java时间API
    private Instant createdAt;
    private Duration duration;
}
```

### 记录类型支持

```java
// Java 17+ 记录类型
public record UserRecord(
    Long id,
    String username,
    String email
) {}

// Jackson 3.x原生支持序列化和反序列化记录类型
@RestController
public class RecordController {

    @PostMapping("/users")
    public UserRecord createUser(@RequestBody UserRecord user) {
        return userService.create(user);
    }
}
```

---

## 测试改进

### 测试上下文暂停

Spring Framework 7可以暂停和恢复测试上下文,节省内存。

```java
@SpringBootTest
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class IntegrationTest {

    @Test
    void test1() {
        // 测试执行
    }

    @PauseContext  // 暂停上下文
    @Test
    void longRunningTest() {
        // 这个测试运行时,其他上下文可以被暂停以节省内存
    }

    @Test
    void test2() {
        // 上下文自动恢复
    }
}
```

---

## 原生镜像支持

### 构建原生镜像

```bash
# 使用Maven构建原生镜像
mvn -Pnative spring-boot:build-image

# 使用Gradle
gradle bootBuildImage
```

### AOT处理配置

```java
@Configuration
public class NativeConfig {

    @Bean
    @RegisterReflectionForBinding(User.class)
    public User userPrototype() {
        // 注册需要反射的类型
        return new User();
    }
}
```

### 性能对比

| 指标 | JVM模式 | 原生镜像 |
|------|---------|----------|
| 启动时间 | ~2.5s | ~0.05s (50倍提升) |
| 内存占用 | ~200MB | ~50MB |
| 镜像大小 | ~150MB | ~80MB |

---

## 最佳实践

### 1. 合理使用弹性机制

```java
@Service
public class BestPracticeService {

    // ✓ 好的做法:针对瞬时故障重试
    @Retryable(
        maxAttempts = 3,
        retryFor = {SocketTimeoutException.class, ConnectException.class}
    )
    public Data fetchFromExternalApi() {
        return apiClient.getData();
    }

    // ✗ 不好的做法:不要对业务异常重试
    @Retryable  // 错误!不应该重试业务异常
    public void transferMoney(Account from, Account to, BigDecimal amount) {
        if (from.getBalance().compareTo(amount) < 0) {
            throw new InsufficientFundsException();  // 重试无意义
        }
    }
}
```

### 2. API版本生命周期管理

```java
/**
 * API版本管理策略:
 * - v1: 稳定版本,2024-01-01发布
 * - v2: 当前版本,2024-06-01发布,新增特性
 * - v3: 预览版本,2024-12-01计划发布
 */
@RestController
@RequestMapping("/api")
public class VersionedApi {

    @GetMapping(value = "/data", version = "v1")
    @Deprecated(since = "2.0", forRemoval = true)
    public ResponseV1 getDataV1() {
        // 计划在2025-06-01移除
    }

    @GetMapping(value = "/data", version = "v2")
    public ResponseV2 getDataV2() {
        // 当前推荐版本
    }
}
```

---

## 总结

Spring Boot 4.x和Spring Framework 7带来了许多激动人心的新特性:

1. **内置弹性**使应用更健壮
2. **API版本控制**简化了API演进
3. **空安全注解**减少了NPE
4. **虚拟线程**实现了更高的并发
5. **原生镜像**提供了更快的启动和更小的占用

这些特性使Spring成为构建现代化、高性能企业应用的理想选择。
