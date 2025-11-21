package com.enterprise.common.core.result;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.io.Serializable;
import java.util.List;

/**
 * Paginated Result
 *
 * @param <T> Data type
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PageResult<T> implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * Current page number (1-based)
     */
    private Integer pageNum;

    /**
     * Page size
     */
    private Integer pageSize;

    /**
     * Total number of records
     */
    private Long total;

    /**
     * Total number of pages
     */
    private Integer pages;

    /**
     * Data list
     */
    private List<T> records;

    /**
     * Has previous page
     */
    private Boolean hasPrevious;

    /**
     * Has next page
     */
    private Boolean hasNext;

    public PageResult(Integer pageNum, Integer pageSize, Long total, List<T> records) {
        this.pageNum = pageNum;
        this.pageSize = pageSize;
        this.total = total;
        this.records = records;
        this.pages = (int) Math.ceil((double) total / pageSize);
        this.hasPrevious = pageNum > 1;
        this.hasNext = pageNum < this.pages;
    }

    /**
     * Create empty page result
     */
    public static <T> PageResult<T> empty(Integer pageNum, Integer pageSize) {
        return new PageResult<>(pageNum, pageSize, 0L, List.of());
    }
}
