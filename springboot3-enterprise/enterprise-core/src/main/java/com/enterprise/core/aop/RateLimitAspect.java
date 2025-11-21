package com.enterprise.core.aop;

import com.enterprise.common.exception.BusinessException;
import com.enterprise.common.result.ResultCode;
import com.enterprise.core.cache.CacheService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;

import java.lang.annotation.*;
import java.util.concurrent.TimeUnit;

/**
 * 限流切面
 */
@Slf4j
@Aspect
@Component
@RequiredArgsConstructor
public class RateLimitAspect {

    private final CacheService cacheService;

    @Around("@annotation(rateLimit)")
    public Object around(ProceedingJoinPoint point, RateLimit rateLimit) throws Throwable {
        MethodSignature signature = (MethodSignature) point.getSignature();
        String key = "rate_limit:" + signature.getDeclaringTypeName() + ":" + signature.getName();

        // 获取当前计数
        Long count = cacheService.increment(key);

        if (count == 1) {
            // 首次访问，设置过期时间
            cacheService.expire(key, rateLimit.time(), TimeUnit.SECONDS);
        }

        if (count > rateLimit.count()) {
            log.warn("Rate limit exceeded for key: {}, count: {}", key, count);
            throw new BusinessException(ResultCode.RATE_LIMIT_EXCEEDED);
        }

        return point.proceed();
    }

    /**
     * 限流注解
     */
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    public @interface RateLimit {
        /**
         * 限流次数
         */
        int count() default 100;

        /**
         * 时间窗口（秒）
         */
        int time() default 60;
    }
}
