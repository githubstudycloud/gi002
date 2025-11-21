package com.enterprise.demo.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.enterprise.common.exception.BusinessException;
import com.enterprise.common.result.ResultCode;
import com.enterprise.core.cache.CacheService;
import com.enterprise.data.base.PageQuery;
import com.enterprise.demo.entity.User;
import com.enterprise.demo.mapper.UserMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 用户服务
 */
@Service
@RequiredArgsConstructor
public class UserService extends ServiceImpl<UserMapper, User> {

    private final CacheService cacheService;

    /**
     * 分页查询用户
     */
    public IPage<User> page(PageQuery query) {
        return this.page(query.toPage());
    }

    /**
     * 根据ID查询用户（带缓存）
     */
    @Cacheable(value = "user", key = "#id")
    public User getById(Long id) {
        return super.getById(id);
    }

    /**
     * 根据用户名查询用户
     */
    public User getByUsername(String username) {
        return this.lambdaQuery()
                .eq(User::getUsername, username)
                .one();
    }

    /**
     * 创建用户
     */
    @Transactional(rollbackFor = Exception.class)
    public User createUser(User user) {
        // 检查用户名是否存在
        User existUser = getByUsername(user.getUsername());
        if (existUser != null) {
            throw new BusinessException(ResultCode.DATA_ALREADY_EXISTS, "用户名已存在");
        }

        // 设置默认值
        if (user.getStatus() == null) {
            user.setStatus(1);
        }

        this.save(user);
        return user;
    }

    /**
     * 更新用户
     */
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = "user", key = "#user.id")
    public User updateUser(User user) {
        this.updateById(user);
        return user;
    }

    /**
     * 删除用户
     */
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = "user", key = "#id")
    public void deleteUser(Long id) {
        this.removeById(id);
    }
}
