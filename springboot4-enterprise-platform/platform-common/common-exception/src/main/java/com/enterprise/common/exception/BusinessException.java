package com.enterprise.common.exception;

import com.enterprise.common.core.result.ResultCode;

/**
 * Business Exception
 * For business logic errors
 */
public class BusinessException extends BaseException {

    private static final long serialVersionUID = 1L;

    public BusinessException(String message) {
        super(ResultCode.BUSINESS_ERROR, message);
    }

    public BusinessException(ResultCode resultCode) {
        super(resultCode);
    }

    public BusinessException(ResultCode resultCode, String message) {
        super(resultCode, message);
    }

    public BusinessException(String message, Throwable cause) {
        super(ResultCode.BUSINESS_ERROR.getCode(), message, cause);
    }
}
