# 开发指南

## Spring Boot 2.x 核心组件功能探究

本项目系统性地整合了 Spring Boot 2.x 生态中的主要组件，以下是各组件的功能说明和使用示例。

## 1. Spring Boot 核心功能

### 1.1 自动配置

Spring Boot 通过 `@SpringBootApplication` 自动配置应用：

```java
@SpringBootApplication
@EnableDiscoveryClient
@MapperScan("com.enterprise.system.mapper")
public class SystemApplication {
    public static void main(String[] args) {
        SpringApplication.run(SystemApplication.class, args);
    }
}
```

### 1.2 配置文件

支持 `application.yml` 和 `application.properties`：

```yaml
spring:
  profiles:
    active: dev
---
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:mysql://localhost:3306/dev_db
---
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: jdbc:mysql://prod-server:3306/prod_db
```

### 1.3 条件注解

```java
@Configuration
public class CustomConfig {

    @Bean
    @ConditionalOnProperty(name = "feature.enabled", havingValue = "true")
    public FeatureService featureService() {
        return new FeatureServiceImpl();
    }

    @Bean
    @ConditionalOnMissingBean
    public DefaultService defaultService() {
        return new DefaultServiceImpl();
    }
}
```

## 2. Spring Web MVC

### 2.1 RESTful API

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public R<Page<User>> list(@RequestParam(defaultValue = "1") int page,
                               @RequestParam(defaultValue = "10") int size) {
        Page<User> userPage = userService.page(new Page<>(page, size));
        return R.ok(userPage);
    }

    @PostMapping
    public R<User> create(@Validated @RequestBody UserDTO dto) {
        User user = userService.create(dto);
        return R.ok(user, "创建成功");
    }

    @PutMapping("/{id}")
    public R<User> update(@PathVariable Long id,
                          @Validated @RequestBody UserDTO dto) {
        User user = userService.update(id, dto);
        return R.ok(user, "更新成功");
    }

    @DeleteMapping("/{id}")
    public R<Void> delete(@PathVariable Long id) {
        userService.delete(id);
        return R.ok(null, "删除成功");
    }
}
```

### 2.2 参数校验

```java
public class UserDTO {

    @NotBlank(message = "用户名不能为空")
    @Length(min = 3, max = 30, message = "用户名长度为3-30个字符")
    private String username;

    @Email(message = "邮箱格式不正确")
    private String email;

    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;

    @Min(value = 0, message = "年龄不能小于0")
    @Max(value = 150, message = "年龄不能大于150")
    private Integer age;
}
```

### 2.3 异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public R<?> handleValidationException(MethodArgumentNotValidException e) {
        FieldError fieldError = e.getBindingResult().getFieldError();
        String message = fieldError != null ? fieldError.getDefaultMessage() : "参数校验失败";
        return R.fail(400, message);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public R<?> handleDataIntegrityException(DataIntegrityViolationException e) {
        return R.fail(409, "数据冲突，该记录可能已存在");
    }
}
```

## 3. Spring Data JPA / MyBatis Plus

### 3.1 MyBatis Plus 基础用法

```java
// Entity
@Data
@TableName("sys_user")
public class SysUser extends BaseEntity {
    @TableId(type = IdType.AUTO)
    private Long userId;

    private String username;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableLogic
    private Integer deleted;
}

// Mapper
@Mapper
public interface SysUserMapper extends BaseMapper<SysUser> {

    @Select("SELECT * FROM sys_user WHERE username = #{username}")
    SysUser findByUsername(@Param("username") String username);

    IPage<SysUser> selectUserPage(Page<SysUser> page, @Param("query") UserQuery query);
}

// Service
@Service
public class SysUserServiceImpl extends ServiceImpl<SysUserMapper, SysUser>
        implements SysUserService {

    @Override
    public List<SysUser> listActiveUsers() {
        return list(Wrappers.<SysUser>lambdaQuery()
                .eq(SysUser::getStatus, 1)
                .orderByDesc(SysUser::getCreateTime));
    }
}
```

### 3.2 分页查询

```java
@GetMapping("/page")
public R<IPage<SysUser>> page(@RequestParam(defaultValue = "1") long current,
                               @RequestParam(defaultValue = "10") long size,
                               UserQuery query) {
    Page<SysUser> page = new Page<>(current, size);

    LambdaQueryWrapper<SysUser> wrapper = Wrappers.lambdaQuery();
    wrapper.like(StringUtils.isNotBlank(query.getUsername()),
                 SysUser::getUsername, query.getUsername())
           .eq(query.getStatus() != null, SysUser::getStatus, query.getStatus())
           .between(query.getStartTime() != null && query.getEndTime() != null,
                    SysUser::getCreateTime, query.getStartTime(), query.getEndTime());

    IPage<SysUser> result = userService.page(page, wrapper);
    return R.ok(result);
}
```

### 3.3 自动填充

```java
@Component
public class MyMetaObjectHandler implements MetaObjectHandler {

    @Override
    public void insertFill(MetaObject metaObject) {
        this.strictInsertFill(metaObject, "createTime", LocalDateTime.class, LocalDateTime.now());
        this.strictInsertFill(metaObject, "createBy", String.class, getCurrentUsername());
    }

    @Override
    public void updateFill(MetaObject metaObject) {
        this.strictUpdateFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());
        this.strictUpdateFill(metaObject, "updateBy", String.class, getCurrentUsername());
    }
}
```

## 4. Spring Security

### 4.1 安全配置

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
            .authorizeRequests()
            .antMatchers("/auth/**", "/actuator/**").permitAll()
            .antMatchers("/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated()
            .and()
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### 4.2 JWT 工具类

```java
@Component
public class JwtTokenUtil {

    @Value("${jwt.secret}")
    private String secret;

    @Value("${jwt.expiration}")
    private Long expiration;

    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("username", userDetails.getUsername());
        claims.put("authorities", userDetails.getAuthorities());

        return Jwts.builder()
                .setClaims(claims)
                .setSubject(userDetails.getUsername())
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + expiration))
                .signWith(Keys.hmacShaKeyFor(secret.getBytes()), SignatureAlgorithm.HS512)
                .compact();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder()
                .setSigningKey(secret.getBytes())
                .build()
                .parseClaimsJws(token);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }
}
```

## 5. Spring Cloud Gateway

### 5.1 路由配置

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: auth-service
          uri: lb://enterprise-auth
          predicates:
            - Path=/auth/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
```

### 5.2 自定义过滤器

```java
@Component
public class AuthGlobalFilter implements GlobalFilter, Ordered {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String token = exchange.getRequest().getHeaders().getFirst("Authorization");

        if (StringUtils.isBlank(token)) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        // 验证 token
        if (!jwtTokenUtil.validateToken(token)) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        return chain.filter(exchange);
    }

    @Override
    public int getOrder() {
        return -100;
    }
}
```

## 6. Spring Cloud Alibaba Nacos

### 6.1 服务注册

```yaml
spring:
  application:
    name: enterprise-system
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
        namespace: public
        group: DEFAULT_GROUP
```

### 6.2 配置中心

```yaml
spring:
  cloud:
    nacos:
      config:
        server-addr: 127.0.0.1:8848
        file-extension: yml
        namespace: public
        group: DEFAULT_GROUP
        shared-configs:
          - data-id: common-config.yml
            refresh: true
```

### 6.3 动态刷新配置

```java
@RefreshScope
@RestController
public class ConfigController {

    @Value("${custom.property:default}")
    private String customProperty;

    @GetMapping("/config")
    public String getConfig() {
        return customProperty;
    }
}
```

## 7. Redis 缓存

### 7.1 注解式缓存

```java
@Service
public class UserService {

    @Cacheable(value = "users", key = "#id")
    public User getUserById(Long id) {
        return userMapper.selectById(id);
    }

    @CachePut(value = "users", key = "#user.id")
    public User updateUser(User user) {
        userMapper.updateById(user);
        return user;
    }

    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userMapper.deleteById(id);
    }

    @CacheEvict(value = "users", allEntries = true)
    public void clearCache() {
        // 清空所有缓存
    }
}
```

### 7.2 Redis 操作

```java
@Service
public class CacheService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    // String 操作
    public void setString(String key, String value, long timeout) {
        redisTemplate.opsForValue().set(key, value, timeout, TimeUnit.SECONDS);
    }

    // Hash 操作
    public void setHash(String key, String field, Object value) {
        redisTemplate.opsForHash().put(key, field, value);
    }

    // List 操作
    public void pushList(String key, Object value) {
        redisTemplate.opsForList().rightPush(key, value);
    }

    // Set 操作
    public void addSet(String key, Object... values) {
        redisTemplate.opsForSet().add(key, values);
    }

    // Sorted Set 操作
    public void addZSet(String key, Object value, double score) {
        redisTemplate.opsForZSet().add(key, value, score);
    }
}
```

## 8. 分布式事务 Seata

### 8.1 配置 Seata

```yaml
seata:
  enabled: true
  application-id: enterprise-system
  tx-service-group: enterprise-group
  registry:
    type: nacos
    nacos:
      server-addr: 127.0.0.1:8848
      namespace: public
      group: SEATA_GROUP
```

### 8.2 使用分布式事务

```java
@Service
public class OrderService {

    @Autowired
    private OrderMapper orderMapper;

    @Autowired
    private StockFeignClient stockFeignClient;

    @GlobalTransactional(name = "create-order", rollbackFor = Exception.class)
    public void createOrder(OrderDTO dto) {
        // 1. 创建订单
        Order order = new Order();
        BeanUtils.copyProperties(dto, order);
        orderMapper.insert(order);

        // 2. 扣减库存（远程调用）
        stockFeignClient.deductStock(dto.getProductId(), dto.getQuantity());

        // 3. 扣减余额（远程调用）
        accountFeignClient.deductBalance(dto.getUserId(), dto.getAmount());
    }
}
```

## 9. 消息队列 RabbitMQ

### 9.1 配置 RabbitMQ

```yaml
spring:
  rabbitmq:
    host: 127.0.0.1
    port: 5672
    username: admin
    password: admin123
    virtual-host: /
```

### 9.2 定义交换机和队列

```java
@Configuration
public class RabbitMQConfig {

    @Bean
    public DirectExchange orderExchange() {
        return new DirectExchange("order.exchange", true, false);
    }

    @Bean
    public Queue orderQueue() {
        return new Queue("order.queue", true);
    }

    @Bean
    public Binding orderBinding() {
        return BindingBuilder.bind(orderQueue())
                .to(orderExchange())
                .with("order.create");
    }
}
```

### 9.3 发送和接收消息

```java
// 生产者
@Service
public class OrderProducer {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void sendOrderMessage(Order order) {
        rabbitTemplate.convertAndSend("order.exchange", "order.create", order);
    }
}

// 消费者
@Component
public class OrderConsumer {

    @RabbitListener(queues = "order.queue")
    public void handleOrder(Order order) {
        log.info("收到订单消息: {}", order);
        // 处理订单逻辑
    }
}
```

## 10. 定时任务

### 10.1 使用 @Scheduled

```java
@Component
public class ScheduledTasks {

    @Scheduled(cron = "0 0 2 * * ?")
    public void cleanExpiredData() {
        log.info("清理过期数据");
        // 清理逻辑
    }

    @Scheduled(fixedRate = 60000)
    public void syncData() {
        log.info("同步数据");
        // 同步逻辑
    }
}
```

### 10.2 动态定时任务

使用 XXL-JOB 或 Quartz 实现动态配置定时任务。

## 11. API 文档 Knife4j

### 11.1 配置 Swagger

```java
@Configuration
@EnableKnife4j
public class Knife4jConfig {

    @Bean
    public Docket api() {
        return new Docket(DocumentationType.OAS_30)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.enterprise"))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("Enterprise API 文档")
                .description("企业级微服务平台接口文档")
                .version("1.0.0")
                .contact(new Contact("Enterprise Team", "", "support@enterprise.com"))
                .build();
    }
}
```

### 11.2 API 注解

```java
@Api(tags = "用户管理")
@RestController
@RequestMapping("/user")
public class UserController {

    @ApiOperation("查询用户列表")
    @ApiImplicitParams({
        @ApiImplicitParam(name = "page", value = "页码", defaultValue = "1"),
        @ApiImplicitParam(name = "size", value = "每页数量", defaultValue = "10")
    })
    @GetMapping("/list")
    public R<Page<User>> list(@RequestParam int page, @RequestParam int size) {
        return R.ok(userService.page(new Page<>(page, size)));
    }

    @ApiOperation("创建用户")
    @PostMapping
    public R<User> create(@ApiParam("用户信息") @RequestBody UserDTO dto) {
        return R.ok(userService.create(dto));
    }
}
```

## 最佳实践

### 1. 代码规范
- 使用 Lombok 减少样板代码
- 统一异常处理
- 统一响应格式
- 合理使用设计模式

### 2. 性能优化
- 合理使用缓存
- 数据库索引优化
- 分页查询
- 异步处理

### 3. 安全建议
- 敏感信息加密
- SQL 防注入
- XSS 防护
- CSRF 防护

---

**最后更新**: 2025-11-20
