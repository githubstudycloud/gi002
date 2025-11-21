package errors

import (
	"fmt"
	"net/http"
)

// ErrorCode 错误码类型
type ErrorCode int

const (
	// 通用错误码 1xxx
	ErrSuccess         ErrorCode = 0
	ErrInternalServer  ErrorCode = 1000
	ErrInvalidParams   ErrorCode = 1001
	ErrNotFound        ErrorCode = 1002
	ErrUnauthorized    ErrorCode = 1003
	ErrForbidden       ErrorCode = 1004
	ErrTooManyRequests ErrorCode = 1005

	// 用户相关错误码 2xxx
	ErrUserNotFound      ErrorCode = 2000
	ErrUserAlreadyExists ErrorCode = 2001
	ErrInvalidPassword   ErrorCode = 2002
	ErrUserDisabled      ErrorCode = 2003

	// 订单相关错误码 3xxx
	ErrOrderNotFound   ErrorCode = 3000
	ErrOrderCancelled  ErrorCode = 3001
	ErrInsufficientStock ErrorCode = 3002

	// 数据库错误码 4xxx
	ErrDatabase        ErrorCode = 4000
	ErrDatabaseConnect ErrorCode = 4001
	ErrDatabaseQuery   ErrorCode = 4002

	// 缓存错误码 5xxx
	ErrCache        ErrorCode = 5000
	ErrCacheConnect ErrorCode = 5001
	ErrCacheGet     ErrorCode = 5002
	ErrCacheSet     ErrorCode = 5003

	// 消息队列错误码 6xxx
	ErrMQ        ErrorCode = 6000
	ErrMQConnect ErrorCode = 6001
	ErrMQPublish ErrorCode = 6002
	ErrMQConsume ErrorCode = 6003
)

// AppError 应用错误
type AppError struct {
	Code    ErrorCode
	Message string
	Err     error
}

// Error 实现 error 接口
func (e *AppError) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("code: %d, message: %s, error: %v", e.Code, e.Message, e.Err)
	}
	return fmt.Sprintf("code: %d, message: %s", e.Code, e.Message)
}

// Unwrap 支持 errors.Unwrap
func (e *AppError) Unwrap() error {
	return e.Err
}

// New 创建新的应用错误
func New(code ErrorCode, message string) *AppError {
	return &AppError{
		Code:    code,
		Message: message,
	}
}

// Wrap 包装错误
func Wrap(code ErrorCode, message string, err error) *AppError {
	return &AppError{
		Code:    code,
		Message: message,
		Err:     err,
	}
}

// HTTPStatus 获取对应的HTTP状态码
func (e *AppError) HTTPStatus() int {
	switch e.Code {
	case ErrSuccess:
		return http.StatusOK
	case ErrInvalidParams:
		return http.StatusBadRequest
	case ErrUnauthorized:
		return http.StatusUnauthorized
	case ErrForbidden:
		return http.StatusForbidden
	case ErrNotFound, ErrUserNotFound, ErrOrderNotFound:
		return http.StatusNotFound
	case ErrTooManyRequests:
		return http.StatusTooManyRequests
	default:
		return http.StatusInternalServerError
	}
}

// 错误消息映射
var errorMessages = map[ErrorCode]string{
	ErrSuccess:           "success",
	ErrInternalServer:    "internal server error",
	ErrInvalidParams:     "invalid parameters",
	ErrNotFound:          "resource not found",
	ErrUnauthorized:      "unauthorized",
	ErrForbidden:         "forbidden",
	ErrTooManyRequests:   "too many requests",
	ErrUserNotFound:      "user not found",
	ErrUserAlreadyExists: "user already exists",
	ErrInvalidPassword:   "invalid password",
	ErrUserDisabled:      "user is disabled",
	ErrOrderNotFound:     "order not found",
	ErrOrderCancelled:    "order is cancelled",
	ErrInsufficientStock: "insufficient stock",
	ErrDatabase:          "database error",
	ErrDatabaseConnect:   "database connection error",
	ErrDatabaseQuery:     "database query error",
	ErrCache:             "cache error",
	ErrCacheConnect:      "cache connection error",
	ErrCacheGet:          "cache get error",
	ErrCacheSet:          "cache set error",
	ErrMQ:                "message queue error",
	ErrMQConnect:         "message queue connection error",
	ErrMQPublish:         "message queue publish error",
	ErrMQConsume:         "message queue consume error",
}

// GetMessage 获取错误消息
func GetMessage(code ErrorCode) string {
	if msg, ok := errorMessages[code]; ok {
		return msg
	}
	return "unknown error"
}

// Response 统一响应结构
type Response struct {
	Code    ErrorCode   `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
}

// Success 成功响应
func Success(data interface{}) *Response {
	return &Response{
		Code:    ErrSuccess,
		Message: GetMessage(ErrSuccess),
		Data:    data,
	}
}

// Fail 失败响应
func Fail(code ErrorCode, message string) *Response {
	if message == "" {
		message = GetMessage(code)
	}
	return &Response{
		Code:    code,
		Message: message,
	}
}
