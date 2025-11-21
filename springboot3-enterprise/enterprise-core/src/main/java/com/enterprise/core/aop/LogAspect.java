package com.enterprise.core.aop;

import cn.hutool.core.util.StrUtil;
import cn.hutool.json.JSONUtil;
import com.enterprise.common.utils.TraceIdUtils;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.multipart.MultipartFile;

import jakarta.servlet.http.HttpServletResponse;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * 日志切面 - 记录接口请求日志
 */
@Slf4j
@Aspect
@Component
public class LogAspect {

    /**
     * 切入点 - 所有Controller层方法
     */
    @Pointcut("execution(* com.enterprise..controller..*.*(..))")
    public void controllerPointcut() {
    }

    @Around("controllerPointcut()")
    public Object around(ProceedingJoinPoint point) throws Throwable {
        long startTime = System.currentTimeMillis();

        // 获取请求信息
        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = attributes != null ? attributes.getRequest() : null;

        // 获取方法信息
        MethodSignature signature = (MethodSignature) point.getSignature();
        String className = point.getTarget().getClass().getSimpleName();
        String methodName = signature.getName();

        // 构建日志信息
        Map<String, Object> logMap = new LinkedHashMap<>();
        logMap.put("traceId", TraceIdUtils.getTraceId());

        if (request != null) {
            logMap.put("url", request.getRequestURI());
            logMap.put("method", request.getMethod());
            logMap.put("ip", getClientIp(request));
        }

        logMap.put("class", className);
        logMap.put("function", methodName);
        logMap.put("params", getParams(point, signature));

        Object result = null;
        Exception exception = null;

        try {
            result = point.proceed();
            return result;
        } catch (Exception e) {
            exception = e;
            throw e;
        } finally {
            long costTime = System.currentTimeMillis() - startTime;
            logMap.put("costTime", costTime + "ms");

            if (exception != null) {
                logMap.put("status", "ERROR");
                logMap.put("errorMsg", exception.getMessage());
                log.error("Request Log: {}", JSONUtil.toJsonStr(logMap));
            } else {
                logMap.put("status", "SUCCESS");
                // 响应结果日志（可选，避免日志过大）
                // logMap.put("result", result);
                log.info("Request Log: {}", JSONUtil.toJsonStr(logMap));
            }
        }
    }

    /**
     * 获取请求参数
     */
    private Map<String, Object> getParams(ProceedingJoinPoint point, MethodSignature signature) {
        Map<String, Object> params = new LinkedHashMap<>();
        String[] paramNames = signature.getParameterNames();
        Object[] paramValues = point.getArgs();

        if (paramNames != null && paramValues != null) {
            for (int i = 0; i < paramNames.length; i++) {
                Object value = paramValues[i];
                // 过滤掉特殊类型
                if (value instanceof HttpServletRequest
                        || value instanceof HttpServletResponse
                        || value instanceof MultipartFile) {
                    continue;
                }
                params.put(paramNames[i], value);
            }
        }
        return params;
    }

    /**
     * 获取客户端IP
     */
    private String getClientIp(HttpServletRequest request) {
        String ip = request.getHeader("X-Forwarded-For");
        if (StrUtil.isBlank(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Proxy-Client-IP");
        }
        if (StrUtil.isBlank(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("WL-Proxy-Client-IP");
        }
        if (StrUtil.isBlank(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("X-Real-IP");
        }
        if (StrUtil.isBlank(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }
        // 多个代理的情况，取第一个IP
        if (ip != null && ip.contains(",")) {
            ip = ip.split(",")[0].trim();
        }
        return ip;
    }
}
