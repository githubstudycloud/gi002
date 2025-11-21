"""
异常处理器
用于FastAPI等Web框架的异常处理
"""

from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .base import BaseException as CustomBaseException


def exception_to_dict(exc: Exception) -> Dict[str, Any]:
    """将异常转换为字典"""
    if isinstance(exc, CustomBaseException):
        return exc.to_dict()
    else:
        return {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc),
                "details": {},
            }
        }


async def custom_exception_handler(request: Request, exc: CustomBaseException) -> JSONResponse:
    """自定义异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """验证异常处理器"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {"errors": errors},
            }
        },
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": {},
            }
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "details": {"type": type(exc).__name__},
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册所有异常处理器到FastAPI应用

    Args:
        app: FastAPI应用实例
    """
    # 自定义异常
    app.add_exception_handler(CustomBaseException, custom_exception_handler)

    # 请求验证异常
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # HTTP异常
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)

    # 通用异常
    app.add_exception_handler(Exception, general_exception_handler)
