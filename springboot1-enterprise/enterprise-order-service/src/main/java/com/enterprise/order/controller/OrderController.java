package com.enterprise.order.controller;

import com.enterprise.common.response.Result;
import com.enterprise.order.entity.Order;
import com.enterprise.order.feign.UserServiceClient;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * 订单控制器
 */
@Slf4j
@Api(tags = "订单管理")
@RestController
@RequestMapping("/order")
public class OrderController {

    @Autowired
    private UserServiceClient userServiceClient;

    @ApiOperation("创建订单")
    @PostMapping("/create")
    public Result<Order> createOrder(@RequestBody Order order) {
        log.info("创建订单: userId={}, productName={}", order.getUserId(), order.getProductName());

        // 调用用户服务验证用户
        Result<?> userResult = userServiceClient.getUser(order.getUserId());
        if (userResult.getCode() != 200) {
            return Result.fail("用户不存在或服务不可用");
        }

        // 模拟创建订单
        order.setId(System.currentTimeMillis());
        order.setOrderNo("ORD" + System.currentTimeMillis());
        order.setStatus(0);
        order.setCreateTime(new Date());
        order.setUpdateTime(new Date());

        return Result.success("订单创建成功", order);
    }

    @ApiOperation("获取订单信息")
    @GetMapping("/{id}")
    public Result<Order> getOrder(@PathVariable Long id) {
        log.info("获取订单信息: {}", id);

        // 模拟查询订单
        Order order = new Order();
        order.setId(id);
        order.setOrderNo("ORD" + id);
        order.setUserId(1L);
        order.setProductName("商品示例");
        order.setQuantity(1);
        order.setAmount(new BigDecimal("99.99"));
        order.setStatus(0);
        order.setCreateTime(new Date());
        order.setUpdateTime(new Date());

        return Result.success(order);
    }

    @ApiOperation("获取订单详情（含用户信息）")
    @GetMapping("/{id}/detail")
    public Result<Map<String, Object>> getOrderDetail(@PathVariable Long id) {
        log.info("获取订单详情: {}", id);

        // 查询订单
        Order order = new Order();
        order.setId(id);
        order.setOrderNo("ORD" + id);
        order.setUserId(1L);
        order.setProductName("商品示例");
        order.setQuantity(1);
        order.setAmount(new BigDecimal("99.99"));
        order.setStatus(0);
        order.setCreateTime(new Date());

        // 调用用户服务获取用户信息
        Result<?> userResult = userServiceClient.getUser(order.getUserId());

        Map<String, Object> data = new HashMap<>();
        data.put("order", order);
        data.put("user", userResult.getData());

        return Result.success(data);
    }

    @ApiOperation("取消订单")
    @PutMapping("/{id}/cancel")
    public Result<?> cancelOrder(@PathVariable Long id) {
        log.info("取消订单: {}", id);

        return Result.success("订单已取消");
    }

    @ApiOperation("健康检查")
    @GetMapping("/health")
    public Result<String> health() {
        return Result.success("Order Service is running");
    }

}
