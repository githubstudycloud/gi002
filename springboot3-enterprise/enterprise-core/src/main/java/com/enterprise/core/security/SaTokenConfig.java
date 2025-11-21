package com.enterprise.core.security;

import cn.dev33.satoken.interceptor.SaInterceptor;
import cn.dev33.satoken.router.SaRouter;
import cn.dev33.satoken.stp.StpUtil;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Sa-Token 配置类
 */
@Configuration
public class SaTokenConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 注册Sa-Token拦截器
        registry.addInterceptor(new SaInterceptor(handle -> {
            // 指定排除路径
            SaRouter.match("/**")
                    .notMatch(
                            "/",
                            "/doc.html",
                            "/webjars/**",
                            "/v3/api-docs/**",
                            "/swagger-resources/**",
                            "/favicon.ico",
                            "/error",
                            "/actuator/**",
                            "/auth/login",
                            "/auth/register",
                            "/test/**"
                    )
                    .check(r -> StpUtil.checkLogin());
        })).addPathPatterns("/**");
    }
}
