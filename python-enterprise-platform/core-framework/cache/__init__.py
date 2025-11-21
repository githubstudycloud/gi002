"""
缓存抽象层 - 统一的缓存访问接口
支持: Redis, Memcached, In-Memory
"""

from .base import CacheBase, CacheConfig
from .redis_cache import RedisCache
from .memory_cache import MemoryCache

__all__ = [
    "CacheBase",
    "CacheConfig",
    "RedisCache",
    "MemoryCache",
]
