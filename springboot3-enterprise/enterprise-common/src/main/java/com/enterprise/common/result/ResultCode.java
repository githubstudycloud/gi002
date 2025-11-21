package com.enterprise.common.result;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 响应状态码枚举
 */
@Getter
@AllArgsConstructor
public enum ResultCode {

    // 成功
    SUCCESS(200, "操作成功"),

    // 客户端错误 4xx
    FAILURE(400, "操作失败"),
    UNAUTHORIZED(401, "未授权"),
    FORBIDDEN(403, "禁止访问"),
    NOT_FOUND(404, "资源不存在"),
    METHOD_NOT_ALLOWED(405, "请求方法不允许"),
    REQUEST_TIMEOUT(408, "请求超时"),
    CONFLICT(409, "资源冲突"),
    GONE(410, "资源已删除"),
    UNSUPPORTED_MEDIA_TYPE(415, "不支持的媒体类型"),
    TOO_MANY_REQUESTS(429, "请求过于频繁"),

    // 服务端错误 5xx
    INTERNAL_SERVER_ERROR(500, "服务器内部错误"),
    NOT_IMPLEMENTED(501, "功能未实现"),
    BAD_GATEWAY(502, "网关错误"),
    SERVICE_UNAVAILABLE(503, "服务不可用"),
    GATEWAY_TIMEOUT(504, "网关超时"),

    // 业务错误 1xxx
    PARAM_ERROR(1001, "参数错误"),
    PARAM_MISSING(1002, "参数缺失"),
    PARAM_TYPE_ERROR(1003, "参数类型错误"),
    PARAM_VALID_ERROR(1004, "参数校验失败"),

    // 认证授权 2xxx
    TOKEN_EXPIRED(2001, "Token已过期"),
    TOKEN_INVALID(2002, "Token无效"),
    TOKEN_MISSING(2003, "Token缺失"),
    LOGIN_FAILED(2004, "登录失败"),
    ACCOUNT_LOCKED(2005, "账号已锁定"),
    ACCOUNT_DISABLED(2006, "账号已禁用"),
    PASSWORD_ERROR(2007, "密码错误"),
    PERMISSION_DENIED(2008, "权限不足"),

    // 数据操作 3xxx
    DATA_NOT_FOUND(3001, "数据不存在"),
    DATA_ALREADY_EXISTS(3002, "数据已存在"),
    DATA_SAVE_FAILED(3003, "数据保存失败"),
    DATA_UPDATE_FAILED(3004, "数据更新失败"),
    DATA_DELETE_FAILED(3005, "数据删除失败"),

    // 文件操作 4xxx
    FILE_NOT_FOUND(4001, "文件不存在"),
    FILE_UPLOAD_FAILED(4002, "文件上传失败"),
    FILE_DOWNLOAD_FAILED(4003, "文件下载失败"),
    FILE_TYPE_NOT_ALLOWED(4004, "文件类型不允许"),
    FILE_SIZE_EXCEEDED(4005, "文件大小超限"),

    // 第三方服务 5xxx
    THIRD_PARTY_ERROR(5001, "第三方服务异常"),
    SMS_SEND_FAILED(5002, "短信发送失败"),
    EMAIL_SEND_FAILED(5003, "邮件发送失败"),
    PAYMENT_FAILED(5004, "支付失败"),

    // 系统限流 6xxx
    RATE_LIMIT_EXCEEDED(6001, "访问频率超限"),
    CONCURRENT_LIMIT_EXCEEDED(6002, "并发数超限"),
    CIRCUIT_BREAKER_OPEN(6003, "服务熔断"),
    SERVICE_DEGRADED(6004, "服务降级");

    /**
     * 状态码
     */
    private final Integer code;

    /**
     * 消息
     */
    private final String message;
}
