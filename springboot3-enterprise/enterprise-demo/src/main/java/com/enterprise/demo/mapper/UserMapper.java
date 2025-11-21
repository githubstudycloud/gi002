package com.enterprise.demo.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.enterprise.demo.entity.User;
import org.apache.ibatis.annotations.Mapper;

/**
 * 用户Mapper
 */
@Mapper
public interface UserMapper extends BaseMapper<User> {
}
