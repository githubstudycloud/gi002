package com.enterprise.order.feign;

import com.enterprise.common.response.Result;
import org.springframework.cloud.netflix.feign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * 用户服务 Feign 客户端
 */
@FeignClient(name = "enterprise-user-service", fallback = UserServiceFallback.class)
public interface UserServiceClient {

    /**
     * 获取用户信息
     */
    @GetMapping("/user/{id}")
    Result<?> getUser(@PathVariable("id") Long id);

}
