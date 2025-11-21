package com.enterprise.user.controller;

import com.enterprise.common.response.Result;
import com.enterprise.common.util.JwtUtil;
import com.enterprise.user.entity.User;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * 用户控制器
 */
@Slf4j
@Api(tags = "用户管理")
@RestController
@RequestMapping("/user")
public class UserController {

    @ApiOperation("用户注册")
    @PostMapping("/register")
    public Result<User> register(@RequestBody User user) {
        log.info("用户注册: {}", user.getUsername());

        // 模拟注册逻辑
        user.setId(System.currentTimeMillis());
        user.setStatus(1);
        user.setCreateTime(new Date());
        user.setUpdateTime(new Date());

        // 密码置空，不返回给前端
        user.setPassword(null);

        return Result.success("注册成功", user);
    }

    @ApiOperation("用户登录")
    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody User user) {
        log.info("用户登录: {}", user.getUsername());

        // 模拟登录验证
        if (!"admin".equals(user.getUsername()) || !"123456".equals(user.getPassword())) {
            return Result.fail("用户名或密码错误");
        }

        // 生成 Token
        String token = JwtUtil.generateToken(user.getUsername());

        Map<String, Object> data = new HashMap<>();
        data.put("token", token);
        data.put("username", user.getUsername());

        return Result.success("登录成功", data);
    }

    @ApiOperation("获取用户信息")
    @GetMapping("/{id}")
    public Result<User> getUser(@PathVariable Long id) {
        log.info("获取用户信息: {}", id);

        // 模拟查询用户
        User user = new User();
        user.setId(id);
        user.setUsername("admin");
        user.setNickname("管理员");
        user.setEmail("admin@example.com");
        user.setMobile("13800138000");
        user.setStatus(1);
        user.setCreateTime(new Date());
        user.setUpdateTime(new Date());

        return Result.success(user);
    }

    @ApiOperation("更新用户信息")
    @PutMapping("/{id}")
    public Result<User> updateUser(@PathVariable Long id, @RequestBody User user) {
        log.info("更新用户信息: {}", id);

        user.setId(id);
        user.setUpdateTime(new Date());

        return Result.success("更新成功", user);
    }

    @ApiOperation("删除用户")
    @DeleteMapping("/{id}")
    public Result<?> deleteUser(@PathVariable Long id) {
        log.info("删除用户: {}", id);

        return Result.success("删除成功");
    }

    @ApiOperation("健康检查")
    @GetMapping("/health")
    public Result<String> health() {
        return Result.success("User Service is running");
    }

}
