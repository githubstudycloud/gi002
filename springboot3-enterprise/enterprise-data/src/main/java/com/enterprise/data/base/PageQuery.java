package com.enterprise.data.base;

import com.baomidou.mybatisplus.core.metadata.OrderItem;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import lombok.Data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * 分页查询参数
 */
@Data
public class PageQuery implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 页码（默认1）
     */
    private Integer pageNum = 1;

    /**
     * 每页大小（默认10）
     */
    private Integer pageSize = 10;

    /**
     * 排序字段
     */
    private String orderBy;

    /**
     * 是否升序（默认true）
     */
    private Boolean isAsc = true;

    /**
     * 转换为MyBatis-Plus的Page对象
     */
    public <T> Page<T> toPage() {
        Page<T> page = new Page<>(pageNum, pageSize);

        // 添加排序
        if (orderBy != null && !orderBy.isEmpty()) {
            List<OrderItem> orderItems = new ArrayList<>();
            if (Boolean.TRUE.equals(isAsc)) {
                orderItems.add(OrderItem.asc(orderBy));
            } else {
                orderItems.add(OrderItem.desc(orderBy));
            }
            page.setOrders(orderItems);
        }

        return page;
    }
}
