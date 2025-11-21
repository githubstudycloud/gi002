"""
依赖注入
提供数据库、缓存等依赖
"""

from functools import lru_cache
import sys
from pathlib import Path

# 添加核心框架到路径
core_path = Path(__file__).parent.parent.parent.parent / "core-framework"
sys.path.insert(0, str(core_path))

from database import SQLDatabase, DatabaseConfig, DatabaseType
from cache import RedisCache, CacheConfig, CacheType
from config.settings import get_settings

_database = None
_cache = None


@lru_cache()
def get_database() -> SQLDatabase:
    """获取数据库实例"""
    global _database
    if _database is None:
        settings = get_settings()
        config = DatabaseConfig(
            type=DatabaseType.POSTGRESQL,
            host=settings.database.postgres_host,
            port=settings.database.postgres_port,
            username=settings.database.postgres_user,
            password=settings.database.postgres_password,
            database=settings.database.postgres_db,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            pool_timeout=settings.database.pool_timeout,
            pool_recycle=settings.database.pool_recycle,
            echo=settings.database.echo_sql,
        )
        _database = SQLDatabase(config)
    return _database


@lru_cache()
def get_cache() -> RedisCache:
    """获取缓存实例"""
    global _cache
    if _cache is None:
        settings = get_settings()
        config = CacheConfig(
            type=CacheType.REDIS,
            host=settings.redis.redis_host,
            port=settings.redis.redis_port,
            password=settings.redis.redis_password,
            db=settings.redis.redis_db,
            max_connections=settings.redis.redis_max_connections,
            socket_timeout=settings.redis.redis_socket_timeout,
            socket_connect_timeout=settings.redis.redis_socket_connect_timeout,
        )
        _cache = RedisCache(config)
    return _cache
