package com.enterprise.common.core.result;

import lombok.Getter;

/**
 * Standard Result Codes
 */
@Getter
public enum ResultCode {

    // Success
    SUCCESS(200, "Success"),

    // Client Errors (4xx)
    BAD_REQUEST(400, "Bad Request"),
    UNAUTHORIZED(401, "Unauthorized"),
    FORBIDDEN(403, "Forbidden"),
    NOT_FOUND(404, "Not Found"),
    METHOD_NOT_ALLOWED(405, "Method Not Allowed"),
    CONFLICT(409, "Conflict"),
    VALIDATION_ERROR(422, "Validation Error"),
    TOO_MANY_REQUESTS(429, "Too Many Requests"),

    // Server Errors (5xx)
    INTERNAL_SERVER_ERROR(500, "Internal Server Error"),
    SERVICE_UNAVAILABLE(503, "Service Unavailable"),
    GATEWAY_TIMEOUT(504, "Gateway Timeout"),

    // Business Errors (1xxx)
    BUSINESS_ERROR(1000, "Business Error"),
    DATA_NOT_FOUND(1001, "Data Not Found"),
    DATA_ALREADY_EXISTS(1002, "Data Already Exists"),
    OPERATION_FAILED(1003, "Operation Failed"),

    // Authentication & Authorization Errors (2xxx)
    TOKEN_EXPIRED(2001, "Token Expired"),
    TOKEN_INVALID(2002, "Token Invalid"),
    INSUFFICIENT_PERMISSIONS(2003, "Insufficient Permissions"),
    ACCOUNT_DISABLED(2004, "Account Disabled"),
    ACCOUNT_LOCKED(2005, "Account Locked"),

    // Database Errors (3xxx)
    DATABASE_ERROR(3000, "Database Error"),
    DUPLICATE_KEY_ERROR(3001, "Duplicate Key Error"),

    // External Service Errors (4xxx)
    EXTERNAL_SERVICE_ERROR(4000, "External Service Error"),
    EXTERNAL_SERVICE_TIMEOUT(4001, "External Service Timeout");

    private final Integer code;
    private final String message;

    ResultCode(Integer code, String message) {
        this.code = code;
        this.message = message;
    }
}
