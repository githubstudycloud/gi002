package com.enterprise.web.filter;

import com.enterprise.common.constants.CommonConstants;
import com.enterprise.common.utils.TraceIdUtils;
import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

/**
 * 链路追踪过滤器
 */
public class TraceIdFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        try {
            // 优先从请求头获取traceId
            String traceId = httpRequest.getHeader(CommonConstants.HEADER_TRACE_ID);
            if (traceId == null || traceId.isEmpty()) {
                traceId = TraceIdUtils.generateTraceId();
            }

            // 设置到MDC
            TraceIdUtils.setTraceId(traceId);

            // 设置响应头
            httpResponse.setHeader(CommonConstants.HEADER_TRACE_ID, traceId);

            chain.doFilter(request, response);
        } finally {
            // 清除MDC
            TraceIdUtils.clearTraceId();
        }
    }
}
