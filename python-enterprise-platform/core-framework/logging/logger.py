"""
企业级日志系统实现
基于structlog的结构化日志
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

import structlog
from structlog.stdlib import LoggerFactory
from structlog.processors import (
    TimeStamper,
    StackInfoRenderer,
    format_exc_info,
    UnicodeDecoder,
)


class Logger:
    """日志封装类"""

    def __init__(self, name: str):
        self._logger = structlog.get_logger(name)
        self.name = name

    def debug(self, event: str, **kwargs: Any) -> None:
        """调试日志"""
        self._logger.debug(event, **kwargs)

    def info(self, event: str, **kwargs: Any) -> None:
        """信息日志"""
        self._logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        """警告日志"""
        self._logger.warning(event, **kwargs)

    def error(self, event: str, **kwargs: Any) -> None:
        """错误日志"""
        self._logger.error(event, **kwargs)

    def critical(self, event: str, **kwargs: Any) -> None:
        """严重错误日志"""
        self._logger.critical(event, **kwargs)

    def exception(self, event: str, **kwargs: Any) -> None:
        """异常日志(自动包含异常信息)"""
        self._logger.exception(event, **kwargs)

    def bind(self, **kwargs: Any) -> "Logger":
        """绑定上下文信息"""
        bound_logger = Logger(self.name)
        bound_logger._logger = self._logger.bind(**kwargs)
        return bound_logger


def configure_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    enable_colors: bool = True,
    service_name: Optional[str] = None,
    environment: str = "development",
) -> None:
    """
    配置日志系统

    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径
        json_format: 是否使用JSON格式
        enable_colors: 是否启用控制台颜色
        service_name: 服务名称
        environment: 环境名称 (development, production, staging)
    """

    # 配置标准库logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )

    # 配置structlog处理器
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # 添加服务信息
    if service_name:
        processors.append(
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            )
        )

    # 选择输出格式
    if json_format:
        processors.append(structlog.processors.JSONRenderer())
    else:
        if enable_colors and sys.stdout.isatty():
            processors.append(structlog.dev.ConsoleRenderer())
        else:
            processors.append(structlog.processors.KeyValueRenderer())

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 配置文件输出
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))

        if json_format:
            formatter = logging.Formatter('%(message)s')
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)

    # 添加全局上下文
    global_context = {
        "environment": environment,
    }
    if service_name:
        global_context["service"] = service_name

    structlog.contextvars.clear_contextvars()
    for key, value in global_context.items():
        structlog.contextvars.bind_contextvars(**{key: value})


def get_logger(name: str) -> Logger:
    """
    获取日志记录器

    Args:
        name: 日志记录器名称(通常使用 __name__)

    Returns:
        Logger实例
    """
    return Logger(name)


# 默认配置
configure_logging()
