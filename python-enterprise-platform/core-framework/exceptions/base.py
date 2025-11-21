"""
自定义异常类定义
"""

from typing import Any, Dict, Optional


class BaseException(Exception):
    """基础异常类"""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class ValidationError(BaseException):
    """验证错误"""

    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class AuthenticationError(BaseException):
    """认证错误"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class AuthorizationError(BaseException):
    """授权错误"""

    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=403,
        )


class NotFoundError(BaseException):
    """资源不存在错误"""

    def __init__(self, message: str = "Resource not found", resource: Optional[str] = None):
        details = {"resource": resource} if resource else {}
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class ConflictError(BaseException):
    """冲突错误"""

    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
            details=details,
        )


class DatabaseError(BaseException):
    """数据库错误"""

    def __init__(self, message: str = "Database error", original_error: Optional[Exception] = None):
        details = {"original_error": str(original_error)} if original_error else {}
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details=details,
        )


class CacheError(BaseException):
    """缓存错误"""

    def __init__(self, message: str = "Cache error", original_error: Optional[Exception] = None):
        details = {"original_error": str(original_error)} if original_error else {}
        super().__init__(
            message=message,
            code="CACHE_ERROR",
            status_code=500,
            details=details,
        )


class MessageQueueError(BaseException):
    """消息队列错误"""

    def __init__(self, message: str = "Message queue error", original_error: Optional[Exception] = None):
        details = {"original_error": str(original_error)} if original_error else {}
        super().__init__(
            message=message,
            code="MESSAGE_QUEUE_ERROR",
            status_code=500,
            details=details,
        )


class ExternalServiceError(BaseException):
    """外部服务错误"""

    def __init__(
        self,
        message: str = "External service error",
        service: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        details = {}
        if service:
            details["service"] = service
        if original_error:
            details["original_error"] = str(original_error)

        super().__init__(
            message=message,
            code="EXTERNAL_SERVICE_ERROR",
            status_code=503,
            details=details,
        )


class RateLimitError(BaseException):
    """限流错误"""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None
    ):
        details = {"retry_after": retry_after} if retry_after else {}
        super().__init__(
            message=message,
            code="RATE_LIMIT_ERROR",
            status_code=429,
            details=details,
        )


class BusinessError(BaseException):
    """业务逻辑错误"""

    def __init__(
        self,
        message: str,
        code: str = "BUSINESS_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=400,
            details=details,
        )


class ConfigurationError(BaseException):
    """配置错误"""

    def __init__(self, message: str = "Configuration error"):
        super().__init__(
            message=message,
            code="CONFIGURATION_ERROR",
            status_code=500,
        )
