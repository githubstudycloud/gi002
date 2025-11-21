package com.enterprise.common.result;

import lombok.Data;
import lombok.experimental.Accessors;

import java.io.Serializable;
import java.util.List;

/**
 * 分页结果封装
 *
 * @param <T> 数据类型
 */
@Data
@Accessors(chain = true)
public class PageResult<T> implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 当前页码
     */
    private Long pageNum;

    /**
     * 每页大小
     */
    private Long pageSize;

    /**
     * 总记录数
     */
    private Long total;

    /**
     * 总页数
     */
    private Long pages;

    /**
     * 数据列表
     */
    private List<T> list;

    /**
     * 是否有上一页
     */
    private Boolean hasPrevious;

    /**
     * 是否有下一页
     */
    private Boolean hasNext;

    public static <T> PageResult<T> of(Long pageNum, Long pageSize, Long total, List<T> list) {
        PageResult<T> result = new PageResult<>();
        result.setPageNum(pageNum);
        result.setPageSize(pageSize);
        result.setTotal(total);
        result.setList(list);

        // 计算总页数
        long pages = total % pageSize == 0 ? total / pageSize : total / pageSize + 1;
        result.setPages(pages);

        // 是否有上一页/下一页
        result.setHasPrevious(pageNum > 1);
        result.setHasNext(pageNum < pages);

        return result;
    }

    public static <T> PageResult<T> empty() {
        return of(1L, 10L, 0L, List.of());
    }
}
