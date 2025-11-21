package com.enterprise.gateway.filter;

import com.alibaba.fastjson.JSON;
import com.enterprise.common.response.Result;
import com.enterprise.common.response.ResultCode;
import com.enterprise.common.util.JwtUtil;
import com.netflix.zuul.ZuulFilter;
import com.netflix.zuul.context.RequestContext;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;

/**
 * 认证过滤器
 */
@Slf4j
@Component
public class AuthFilter extends ZuulFilter {

    /**
     * 过滤器类型：pre（路由前）
     */
    @Override
    public String filterType() {
        return "pre";
    }

    /**
     * 过滤器顺序
     */
    @Override
    public int filterOrder() {
        return 1;
    }

    /**
     * 是否执行过滤器
     */
    @Override
    public boolean shouldFilter() {
        RequestContext ctx = RequestContext.getCurrentContext();
        HttpServletRequest request = ctx.getRequest();
        String uri = request.getRequestURI();

        // 登录接口不需要验证
        if (uri.contains("/login") || uri.contains("/register")) {
            return false;
        }

        return true;
    }

    /**
     * 过滤器逻辑
     */
    @Override
    public Object run() {
        RequestContext ctx = RequestContext.getCurrentContext();
        HttpServletRequest request = ctx.getRequest();

        String token = request.getHeader("Authorization");

        if (StringUtils.isBlank(token)) {
            log.warn("请求未携带Token: {}", request.getRequestURI());
            handleUnauthorized(ctx, "未授权，请先登录");
            return null;
        }

        // 验证 Token
        if (!JwtUtil.validateToken(token)) {
            log.warn("Token验证失败: {}", token);
            handleUnauthorized(ctx, "Token无效或已过期");
            return null;
        }

        // 将用户信息传递给下游服务
        try {
            String userId = JwtUtil.getSubject(token);
            ctx.addZuulRequestHeader("X-User-Id", userId);
        } catch (Exception e) {
            log.error("解析Token失败", e);
            handleUnauthorized(ctx, "Token解析失败");
        }

        return null;
    }

    /**
     * 处理未授权请求
     */
    private void handleUnauthorized(RequestContext ctx, String message) {
        ctx.setSendZuulResponse(false);
        ctx.setResponseStatusCode(401);
        ctx.setResponseBody(JSON.toJSONString(Result.fail(ResultCode.UNAUTHORIZED.getCode(), message)));
        ctx.getResponse().setContentType("application/json;charset=UTF-8");
    }

}
