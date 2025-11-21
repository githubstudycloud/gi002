package com.enterprise.demo.controller;

import com.enterprise.common.result.Result;
import com.enterprise.core.cache.CacheService;
import com.enterprise.mq.message.BaseMessage;
import com.enterprise.mq.producer.MessageProducer;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 测试接口（无需登录）
 */
@Tag(name = "测试接口")
@RestController
@RequestMapping("/test")
@RequiredArgsConstructor
public class TestController {

    private final CacheService cacheService;
    private final MessageProducer messageProducer;

    @Operation(summary = "健康检查")
    @GetMapping("/health")
    public Result<String> health() {
        return Result.success("OK");
    }

    @Operation(summary = "测试Redis缓存")
    @PostMapping("/cache")
    public Result<Map<String, Object>> testCache(
            @RequestParam String key,
            @RequestParam String value) {
        // 设置缓存
        cacheService.setMinutes(key, value, 10);

        // 获取缓存
        String cachedValue = cacheService.get(key);

        Map<String, Object> result = new HashMap<>();
        result.put("key", key);
        result.put("value", cachedValue);
        result.put("ttl", cacheService.getExpire(key));

        return Result.success(result);
    }

    @Operation(summary = "测试消息发送")
    @PostMapping("/message")
    public Result<String> testMessage(
            @RequestParam String type,
            @RequestParam String content) {
        BaseMessage message = BaseMessage.of(type, content);
        messageProducer.sendDefault(message);
        return Result.success("消息已发送: " + message.getMessageId());
    }

    @Operation(summary = "测试异常处理")
    @GetMapping("/error")
    public Result<Void> testError(@RequestParam(defaultValue = "business") String type) {
        if ("business".equals(type)) {
            throw new com.enterprise.common.exception.BusinessException("测试业务异常");
        } else if ("system".equals(type)) {
            throw new com.enterprise.common.exception.SystemException("测试系统异常");
        } else {
            throw new RuntimeException("测试运行时异常");
        }
    }

    @Operation(summary = "获取系统信息")
    @GetMapping("/info")
    public Result<Map<String, Object>> info() {
        Map<String, Object> info = new HashMap<>();
        info.put("java.version", System.getProperty("java.version"));
        info.put("os.name", System.getProperty("os.name"));
        info.put("user.timezone", System.getProperty("user.timezone"));
        info.put("available.processors", Runtime.getRuntime().availableProcessors());
        info.put("total.memory", Runtime.getRuntime().totalMemory() / 1024 / 1024 + "MB");
        info.put("free.memory", Runtime.getRuntime().freeMemory() / 1024 / 1024 + "MB");
        return Result.success(info);
    }
}
