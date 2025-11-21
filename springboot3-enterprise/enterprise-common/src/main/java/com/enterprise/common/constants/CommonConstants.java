package com.enterprise.common.constants;

/**
 * 公共常量
 */
public class CommonConstants {

    private CommonConstants() {
    }

    // ==================== 系统常量 ====================
    /**
     * UTF-8 编码
     */
    public static final String UTF8 = "UTF-8";

    /**
     * JSON 类型
     */
    public static final String CONTENT_TYPE_JSON = "application/json;charset=UTF-8";

    /**
     * 成功标记
     */
    public static final Integer SUCCESS = 200;

    /**
     * 失败标记
     */
    public static final Integer FAIL = 500;

    // ==================== 布尔常量 ====================
    /**
     * 是
     */
    public static final Integer YES = 1;

    /**
     * 否
     */
    public static final Integer NO = 0;

    // ==================== 状态常量 ====================
    /**
     * 正常状态
     */
    public static final Integer STATUS_NORMAL = 1;

    /**
     * 禁用状态
     */
    public static final Integer STATUS_DISABLED = 0;

    /**
     * 删除状态
     */
    public static final Integer STATUS_DELETED = -1;

    // ==================== 时间常量 ====================
    /**
     * 默认日期格式
     */
    public static final String DEFAULT_DATE_FORMAT = "yyyy-MM-dd";

    /**
     * 默认时间格式
     */
    public static final String DEFAULT_TIME_FORMAT = "HH:mm:ss";

    /**
     * 默认日期时间格式
     */
    public static final String DEFAULT_DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss";

    /**
     * 默认时区
     */
    public static final String DEFAULT_TIME_ZONE = "Asia/Shanghai";

    // ==================== 分页常量 ====================
    /**
     * 默认页码
     */
    public static final Integer DEFAULT_PAGE_NUM = 1;

    /**
     * 默认每页大小
     */
    public static final Integer DEFAULT_PAGE_SIZE = 10;

    /**
     * 最大每页大小
     */
    public static final Integer MAX_PAGE_SIZE = 1000;

    // ==================== 请求头常量 ====================
    /**
     * 认证请求头
     */
    public static final String HEADER_AUTHORIZATION = "Authorization";

    /**
     * Token 前缀
     */
    public static final String TOKEN_PREFIX = "Bearer ";

    /**
     * 请求ID
     */
    public static final String HEADER_TRACE_ID = "X-Trace-Id";

    /**
     * 用户ID
     */
    public static final String HEADER_USER_ID = "X-User-Id";

    /**
     * 租户ID
     */
    public static final String HEADER_TENANT_ID = "X-Tenant-Id";

    // ==================== 缓存常量 ====================
    /**
     * 默认缓存时间(秒)
     */
    public static final Integer DEFAULT_CACHE_SECONDS = 3600;

    /**
     * 缓存键前缀
     */
    public static final String CACHE_PREFIX = "enterprise:";

    // ==================== 正则表达式 ====================
    /**
     * 手机号正则
     */
    public static final String REGEX_MOBILE = "^1[3-9]\\d{9}$";

    /**
     * 邮箱正则
     */
    public static final String REGEX_EMAIL = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";

    /**
     * 身份证正则
     */
    public static final String REGEX_ID_CARD = "^[1-9]\\d{5}(18|19|20)\\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])\\d{3}[\\dXx]$";
}
