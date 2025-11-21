"""
内存缓存实现 - 适用于单机测试和开发环境
"""

from typing import Any, Optional, List
import time
import asyncio
from collections import OrderedDict
from dataclasses import dataclass

from .base import CacheBase, CacheConfig


@dataclass
class CacheItem:
    """缓存项"""
    value: Any
    expire_at: Optional[float] = None


class MemoryCache(CacheBase):
    """内存缓存实现 - 使用LRU策略"""

    def __init__(self, config: CacheConfig, max_size: int = 10000):
        super().__init__(config)
        self._cache: OrderedDict[str, CacheItem] = OrderedDict()
        self._max_size = max_size
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        """连接缓存(内存缓存无需实际连接)"""
        self._connected = True

    async def disconnect(self) -> None:
        """断开连接"""
        await self.flush()
        self._connected = False

    def _is_expired(self, item: CacheItem) -> bool:
        """检查是否过期"""
        if item.expire_at is None:
            return False
        return time.time() > item.expire_at

    async def _evict_expired(self) -> None:
        """清除过期项"""
        current_time = time.time()
        expired_keys = [
            key for key, item in self._cache.items()
            if item.expire_at and current_time > item.expire_at
        ]
        for key in expired_keys:
            del self._cache[key]

    async def _evict_lru(self) -> None:
        """LRU淘汰"""
        if len(self._cache) >= self._max_size:
            # 删除最旧的项
            self._cache.popitem(last=False)

    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            await self._evict_expired()

            if key not in self._cache:
                return None

            item = self._cache[key]
            if self._is_expired(item):
                del self._cache[key]
                return None

            # 移到末尾(最近使用)
            self._cache.move_to_end(key)
            return item.value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            await self._evict_lru()

            expire_time = ttl if ttl is not None else self.config.default_ttl
            expire_at = time.time() + expire_time if expire_time else None

            self._cache[key] = CacheItem(value=value, expire_at=expire_at)
            self._cache.move_to_end(key)
            return True

    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            await self._evict_expired()
            if key not in self._cache:
                return False

            item = self._cache[key]
            if self._is_expired(item):
                del self._cache[key]
                return False

            return True

    async def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            if key not in self._cache:
                return False

            item = self._cache[key]
            item.expire_at = time.time() + ttl
            return True

    async def ttl(self, key: str) -> int:
        """获取键的剩余生存时间"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            if key not in self._cache:
                return -2  # 键不存在

            item = self._cache[key]
            if item.expire_at is None:
                return -1  # 永不过期

            remaining = int(item.expire_at - time.time())
            return remaining if remaining > 0 else -2

    async def keys(self, pattern: str = "*") -> List[str]:
        """获取匹配的键列表"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            await self._evict_expired()

            if pattern == "*":
                return list(self._cache.keys())

            # 简单的模式匹配
            import fnmatch
            return [key for key in self._cache.keys() if fnmatch.fnmatch(key, pattern)]

    async def flush(self) -> bool:
        """清空所有缓存"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            self._cache.clear()
            return True

    async def incr(self, key: str, amount: int = 1) -> int:
        """递增"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            if key not in self._cache:
                self._cache[key] = CacheItem(value=0)

            item = self._cache[key]
            if not isinstance(item.value, int):
                raise ValueError(f"Key {key} does not contain an integer")

            item.value += amount
            return item.value

    async def decr(self, key: str, amount: int = 1) -> int:
        """递减"""
        if not self._connected:
            raise RuntimeError("Cache not connected")

        async with self._lock:
            if key not in self._cache:
                self._cache[key] = CacheItem(value=0)

            item = self._cache[key]
            if not isinstance(item.value, int):
                raise ValueError(f"Key {key} does not contain an integer")

            item.value -= amount
            return item.value

    def size(self) -> int:
        """获取缓存大小"""
        return len(self._cache)
