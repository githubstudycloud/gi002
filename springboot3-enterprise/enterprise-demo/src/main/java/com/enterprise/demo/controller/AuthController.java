package com.enterprise.demo.controller;

import cn.dev33.satoken.stp.StpUtil;
import com.enterprise.common.exception.BusinessException;
import com.enterprise.common.result.Result;
import com.enterprise.common.result.ResultCode;
import com.enterprise.demo.entity.User;
import com.enterprise.demo.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 认证接口
 */
@Tag(name = "认证管理")
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserService userService;

    @Operation(summary = "用户登录")
    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody LoginRequest request) {
        // 查询用户
        User user = userService.getByUsername(request.getUsername());
        if (user == null) {
            throw new BusinessException(ResultCode.LOGIN_FAILED, "用户不存在");
        }

        // 验证密码（实际应使用加密比对）
        if (!request.getPassword().equals(user.getPassword())) {
            throw new BusinessException(ResultCode.PASSWORD_ERROR);
        }

        // 检查状态
        if (user.getStatus() != 1) {
            throw new BusinessException(ResultCode.ACCOUNT_DISABLED);
        }

        // 登录
        StpUtil.login(user.getId());

        // 返回Token信息
        Map<String, Object> result = new HashMap<>();
        result.put("token", StpUtil.getTokenValue());
        result.put("tokenName", StpUtil.getTokenName());
        result.put("userId", user.getId());
        result.put("username", user.getUsername());
        result.put("nickname", user.getNickname());

        return Result.success(result);
    }

    @Operation(summary = "用户登出")
    @PostMapping("/logout")
    public Result<Void> logout() {
        StpUtil.logout();
        return Result.success();
    }

    @Operation(summary = "获取当前登录用户信息")
    @GetMapping("/info")
    public Result<Map<String, Object>> info() {
        Long userId = StpUtil.getLoginIdAsLong();
        User user = userService.getById(userId);

        Map<String, Object> result = new HashMap<>();
        result.put("userId", user.getId());
        result.put("username", user.getUsername());
        result.put("nickname", user.getNickname());
        result.put("email", user.getEmail());
        result.put("phone", user.getPhone());
        result.put("avatar", user.getAvatar());

        return Result.success(result);
    }

    @Operation(summary = "检查登录状态")
    @GetMapping("/check")
    public Result<Map<String, Object>> checkLogin() {
        Map<String, Object> result = new HashMap<>();
        result.put("isLogin", StpUtil.isLogin());
        if (StpUtil.isLogin()) {
            result.put("userId", StpUtil.getLoginId());
            result.put("tokenTimeout", StpUtil.getTokenTimeout());
        }
        return Result.success(result);
    }

    @Data
    public static class LoginRequest {
        private String username;
        private String password;
    }
}
