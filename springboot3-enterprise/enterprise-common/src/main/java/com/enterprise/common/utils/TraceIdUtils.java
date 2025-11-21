package com.enterprise.common.utils;

import cn.hutool.core.util.IdUtil;
import org.slf4j.MDC;

/**
 * 链路追踪工具类
 */
public class TraceIdUtils {

    private TraceIdUtils() {
    }

    public static final String TRACE_ID = "traceId";

    /**
     * 生成traceId
     */
    public static String generateTraceId() {
        return IdUtil.fastSimpleUUID();
    }

    /**
     * 获取当前traceId
     */
    public static String getTraceId() {
        return MDC.get(TRACE_ID);
    }

    /**
     * 设置traceId
     */
    public static void setTraceId(String traceId) {
        MDC.put(TRACE_ID, traceId);
    }

    /**
     * 清除traceId
     */
    public static void clearTraceId() {
        MDC.remove(TRACE_ID);
    }

    /**
     * 生成并设置traceId
     */
    public static String generateAndSetTraceId() {
        String traceId = generateTraceId();
        setTraceId(traceId);
        return traceId;
    }
}
