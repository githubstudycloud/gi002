package com.enterprise.common.core.constant;

/**
 * Common Constants
 */
public interface CommonConstants {

    /**
     * Default page size
     */
    Integer DEFAULT_PAGE_SIZE = 10;

    /**
     * Max page size
     */
    Integer MAX_PAGE_SIZE = 100;

    /**
     * UTF-8 Charset
     */
    String UTF8 = "UTF-8";

    /**
     * Success status
     */
    String SUCCESS = "success";

    /**
     * Failure status
     */
    String FAILURE = "failure";

    /**
     * Token prefix
     */
    String TOKEN_PREFIX = "Bearer ";

    /**
     * Token header name
     */
    String TOKEN_HEADER = "Authorization";

    /**
     * Trace ID header
     */
    String TRACE_ID_HEADER = "X-Trace-Id";

    /**
     * Request ID header
     */
    String REQUEST_ID_HEADER = "X-Request-Id";

    /**
     * API version header
     */
    String API_VERSION_HEADER = "X-API-Version";

    /**
     * Default API version
     */
    String DEFAULT_API_VERSION = "v1";

    /**
     * Cache prefix
     */
    interface CachePrefix {
        String USER = "user:";
        String TOKEN = "token:";
        String CAPTCHA = "captcha:";
        String PERMISSION = "permission:";
    }

    /**
     * Date format patterns
     */
    interface DatePattern {
        String DATETIME = "yyyy-MM-dd HH:mm:ss";
        String DATE = "yyyy-MM-dd";
        String TIME = "HH:mm:ss";
        String DATETIME_MS = "yyyy-MM-dd HH:mm:ss.SSS";
    }
}
