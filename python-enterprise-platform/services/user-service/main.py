"""
用户服务 - 主入口
提供用户管理、认证、授权功能
"""

import sys
from pathlib import Path

# 添加核心框架到路径
core_path = Path(__file__).parent.parent.parent / "core-framework"
sys.path.insert(0, str(core_path))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import get_settings
from logging.logger import get_logger, configure_logging
from exceptions import register_exception_handlers
from auth.jwt_handler import initialize_jwt_handler

from app.api import router as api_router
from app.dependencies import get_database, get_cache

# 初始化日志
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    settings = get_settings()

    # 启动时初始化
    logger.info("Starting User Service", version="1.0.0")

    # 初始化JWT处理器
    initialize_jwt_handler(
        secret_key=settings.app.secret_key,
        access_token_expire_minutes=settings.app.access_token_expire_minutes,
        refresh_token_expire_days=settings.app.refresh_token_expire_days,
    )

    # 初始化数据库连接
    db = get_database()
    await db.connect()
    logger.info("Database connected")

    # 初始化缓存连接
    cache = get_cache()
    await cache.connect()
    logger.info("Cache connected")

    yield

    # 关闭时清理
    logger.info("Shutting down User Service")
    await cache.disconnect()
    await db.disconnect()


# 创建FastAPI应用
app = FastAPI(
    title="User Service",
    description="企业级用户管理服务",
    version="1.0.0",
    lifespan=lifespan,
)

# 获取配置
settings = get_settings()

# 配置日志
configure_logging(
    level=settings.log.log_level,
    log_file=settings.log.log_file,
    json_format=settings.log.log_json_format,
    enable_colors=settings.log.log_enable_colors,
    service_name="user-service",
    environment=settings.app.environment,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
register_exception_handlers(app)

# 注册路由
app.include_router(api_router, prefix=settings.app.api_prefix)


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "user-service",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "User Service API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.debug,
        workers=1 if settings.app.debug else settings.app.workers,
    )
