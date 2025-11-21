package com.enterprise.order.feign;

import com.enterprise.common.response.Result;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

/**
 * 用户服务降级处理
 */
@Slf4j
@Component
public class UserServiceFallback implements UserServiceClient {

    @Override
    public Result<?> getUser(Long id) {
        log.error("调用用户服务失败，触发降级，用户ID: {}", id);
        return Result.fail("用户服务暂时不可用");
    }

}
