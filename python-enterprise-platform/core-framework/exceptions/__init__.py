"""
统一异常处理模块
定义企业级异常类和处理器
"""

from .base import (
    BaseException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    DatabaseError,
    CacheError,
    MessageQueueError,
    ExternalServiceError,
    RateLimitError,
)

from .handlers import (
    register_exception_handlers,
    exception_to_dict,
)

__all__ = [
    "BaseException",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    "DatabaseError",
    "CacheError",
    "MessageQueueError",
    "ExternalServiceError",
    "RateLimitError",
    "register_exception_handlers",
    "exception_to_dict",
]
