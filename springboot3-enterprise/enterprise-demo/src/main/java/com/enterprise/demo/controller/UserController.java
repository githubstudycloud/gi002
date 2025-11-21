package com.enterprise.demo.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.enterprise.common.result.PageResult;
import com.enterprise.common.result.Result;
import com.enterprise.data.base.PageQuery;
import com.enterprise.demo.entity.User;
import com.enterprise.demo.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

/**
 * 用户管理接口
 */
@Tag(name = "用户管理")
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @Operation(summary = "分页查询用户")
    @GetMapping
    public Result<PageResult<User>> page(PageQuery query) {
        IPage<User> page = userService.page(query);
        PageResult<User> result = PageResult.of(
                page.getCurrent(),
                page.getSize(),
                page.getTotal(),
                page.getRecords()
        );
        return Result.success(result);
    }

    @Operation(summary = "根据ID查询用户")
    @GetMapping("/{id}")
    public Result<User> getById(@Parameter(description = "用户ID") @PathVariable Long id) {
        User user = userService.getById(id);
        return Result.success(user);
    }

    @Operation(summary = "创建用户")
    @PostMapping
    public Result<User> create(@Valid @RequestBody User user) {
        User created = userService.createUser(user);
        return Result.success(created);
    }

    @Operation(summary = "更新用户")
    @PutMapping("/{id}")
    public Result<User> update(
            @Parameter(description = "用户ID") @PathVariable Long id,
            @Valid @RequestBody User user) {
        user.setId(id);
        User updated = userService.updateUser(user);
        return Result.success(updated);
    }

    @Operation(summary = "删除用户")
    @DeleteMapping("/{id}")
    public Result<Void> delete(@Parameter(description = "用户ID") @PathVariable Long id) {
        userService.deleteUser(id);
        return Result.success();
    }
}
