package com.enterprise.auth.controller;

import com.enterprise.common.core.domain.R;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 认证授权控制器
 */
@Slf4j
@RestController
@RequestMapping("/auth")
public class AuthController {

    /**
     * 登录接口
     */
    @PostMapping("/login")
    public R<Map<String, Object>> login(@RequestParam String username, @RequestParam String password) {
        log.info("用户登录: {}", username);

        // TODO: 实现真实的登录逻辑
        Map<String, Object> result = new HashMap<>();
        result.put("token", "mock-jwt-token-" + System.currentTimeMillis());
        result.put("username", username);
        result.put("expiresIn", 1800000);

        return R.ok(result, "登录成功");
    }

    /**
     * 登出接口
     */
    @PostMapping("/logout")
    public R<Void> logout() {
        log.info("用户登出");
        return R.ok(null, "登出成功");
    }

    /**
     * 刷新Token
     */
    @PostMapping("/refresh")
    public R<Map<String, Object>> refresh(@RequestParam String refreshToken) {
        log.info("刷新Token: {}", refreshToken);

        Map<String, Object> result = new HashMap<>();
        result.put("token", "new-mock-jwt-token-" + System.currentTimeMillis());
        result.put("expiresIn", 1800000);

        return R.ok(result, "Token刷新成功");
    }

    /**
     * 获取用户信息
     */
    @GetMapping("/info")
    public R<Map<String, Object>> getUserInfo() {
        Map<String, Object> userInfo = new HashMap<>();
        userInfo.put("userId", 1L);
        userInfo.put("username", "admin");
        userInfo.put("nickname", "管理员");
        userInfo.put("roles", new String[]{"admin"});
        userInfo.put("permissions", new String[]{"*:*:*"});

        return R.ok(userInfo);
    }
}
