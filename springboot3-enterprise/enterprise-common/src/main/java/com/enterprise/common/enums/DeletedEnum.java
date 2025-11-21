package com.enterprise.common.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 删除状态枚举
 */
@Getter
@AllArgsConstructor
public enum DeletedEnum {

    NORMAL(0, "正常"),
    DELETED(1, "已删除");

    private final Integer code;
    private final String desc;
}
