package com.enterprise.common.utils;

import com.enterprise.common.exception.BusinessException;
import com.enterprise.common.result.ResultCode;
import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.ObjectUtil;
import cn.hutool.core.util.StrUtil;

import java.util.Collection;
import java.util.Map;

/**
 * 断言工具类 - 用于参数校验
 */
public class AssertUtils {

    private AssertUtils() {
    }

    /**
     * 断言对象不为空
     */
    public static void notNull(Object object, String message) {
        if (ObjectUtil.isNull(object)) {
            throw new BusinessException(ResultCode.PARAM_ERROR, message);
        }
    }

    /**
     * 断言对象不为空
     */
    public static void notNull(Object object, ResultCode resultCode) {
        if (ObjectUtil.isNull(object)) {
            throw new BusinessException(resultCode);
        }
    }

    /**
     * 断言字符串不为空
     */
    public static void notBlank(String str, String message) {
        if (StrUtil.isBlank(str)) {
            throw new BusinessException(ResultCode.PARAM_ERROR, message);
        }
    }

    /**
     * 断言字符串不为空
     */
    public static void notBlank(String str, ResultCode resultCode) {
        if (StrUtil.isBlank(str)) {
            throw new BusinessException(resultCode);
        }
    }

    /**
     * 断言集合不为空
     */
    public static void notEmpty(Collection<?> collection, String message) {
        if (CollUtil.isEmpty(collection)) {
            throw new BusinessException(ResultCode.PARAM_ERROR, message);
        }
    }

    /**
     * 断言Map不为空
     */
    public static void notEmpty(Map<?, ?> map, String message) {
        if (CollUtil.isEmpty(map)) {
            throw new BusinessException(ResultCode.PARAM_ERROR, message);
        }
    }

    /**
     * 断言条件为真
     */
    public static void isTrue(boolean expression, String message) {
        if (!expression) {
            throw new BusinessException(ResultCode.PARAM_ERROR, message);
        }
    }

    /**
     * 断言条件为真
     */
    public static void isTrue(boolean expression, ResultCode resultCode) {
        if (!expression) {
            throw new BusinessException(resultCode);
        }
    }

    /**
     * 断言条件为假
     */
    public static void isFalse(boolean expression, String message) {
        if (expression) {
            throw new BusinessException(ResultCode.PARAM_ERROR, message);
        }
    }

    /**
     * 断言数据存在
     */
    public static void exists(Object object, String message) {
        if (ObjectUtil.isNull(object)) {
            throw new BusinessException(ResultCode.DATA_NOT_FOUND, message);
        }
    }

    /**
     * 断言数据不存在(用于新增校验)
     */
    public static void notExists(Object object, String message) {
        if (ObjectUtil.isNotNull(object)) {
            throw new BusinessException(ResultCode.DATA_ALREADY_EXISTS, message);
        }
    }

    /**
     * 抛出业务异常
     */
    public static void fail(String message) {
        throw new BusinessException(message);
    }

    /**
     * 抛出业务异常
     */
    public static void fail(ResultCode resultCode) {
        throw new BusinessException(resultCode);
    }

    /**
     * 抛出业务异常
     */
    public static void fail(ResultCode resultCode, String message) {
        throw new BusinessException(resultCode, message);
    }
}
