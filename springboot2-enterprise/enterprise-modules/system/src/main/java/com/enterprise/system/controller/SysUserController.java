package com.enterprise.system.controller;

import com.enterprise.common.core.domain.R;
import com.enterprise.system.domain.SysUser;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

/**
 * 用户管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/user")
public class SysUserController {

    /**
     * 查询用户列表
     */
    @GetMapping("/list")
    public R<List<SysUser>> list() {
        log.info("查询用户列表");

        List<SysUser> users = new ArrayList<>();
        SysUser user = new SysUser();
        user.setUserId(1L);
        user.setUsername("admin");
        user.setNickname("管理员");
        user.setEmail("admin@enterprise.com");
        user.setPhone("18888888888");
        user.setSex(1);
        user.setStatus(1);
        users.add(user);

        return R.ok(users);
    }

    /**
     * 根据ID查询用户
     */
    @GetMapping("/{userId}")
    public R<SysUser> getById(@PathVariable Long userId) {
        log.info("查询用户: {}", userId);

        SysUser user = new SysUser();
        user.setUserId(userId);
        user.setUsername("admin");
        user.setNickname("管理员");
        user.setEmail("admin@enterprise.com");
        user.setPhone("18888888888");
        user.setSex(1);
        user.setStatus(1);

        return R.ok(user);
    }

    /**
     * 新增用户
     */
    @PostMapping
    public R<Void> add(@RequestBody SysUser user) {
        log.info("新增用户: {}", user.getUsername());
        return R.ok(null, "新增成功");
    }

    /**
     * 修改用户
     */
    @PutMapping
    public R<Void> update(@RequestBody SysUser user) {
        log.info("修改用户: {}", user.getUserId());
        return R.ok(null, "修改成功");
    }

    /**
     * 删除用户
     */
    @DeleteMapping("/{userId}")
    public R<Void> delete(@PathVariable Long userId) {
        log.info("删除用户: {}", userId);
        return R.ok(null, "删除成功");
    }
}
