"""
缓存模块测试
"""

import pytest
import asyncio
import sys
from pathlib import Path

# 添加核心框架到路径
core_path = Path(__file__).parent.parent / "core-framework"
sys.path.insert(0, str(core_path))

from cache import MemoryCache, CacheConfig, CacheType


@pytest.mark.asyncio
async def test_memory_cache_basic():
    """测试内存缓存基本操作"""
    config = CacheConfig(type=CacheType.MEMORY)
    cache = MemoryCache(config)

    await cache.connect()
    assert cache.is_connected

    # 设置值
    await cache.set("key1", "value1")
    assert await cache.exists("key1")

    # 获取值
    value = await cache.get("key1")
    assert value == "value1"

    # 删除值
    await cache.delete("key1")
    assert not await cache.exists("key1")

    await cache.disconnect()


@pytest.mark.asyncio
async def test_memory_cache_ttl():
    """测试缓存过期"""
    config = CacheConfig(type=CacheType.MEMORY, default_ttl=1)
    cache = MemoryCache(config)

    await cache.connect()

    # 设置带TTL的值
    await cache.set("temp_key", "temp_value", ttl=1)
    assert await cache.exists("temp_key")

    # 等待过期
    await asyncio.sleep(2)
    assert not await cache.exists("temp_key")

    await cache.disconnect()


@pytest.mark.asyncio
async def test_memory_cache_operations():
    """测试缓存其他操作"""
    config = CacheConfig(type=CacheType.MEMORY)
    cache = MemoryCache(config)

    await cache.connect()

    # 递增
    await cache.set("counter", 0)
    result = await cache.incr("counter", 5)
    assert result == 5

    result = await cache.incr("counter", 3)
    assert result == 8

    # 递减
    result = await cache.decr("counter", 2)
    assert result == 6

    # 键列表
    await cache.set("test1", "value1")
    await cache.set("test2", "value2")
    keys = await cache.keys("test*")
    assert len(keys) >= 2

    # 清空
    await cache.flush()
    keys = await cache.keys()
    assert len(keys) == 0

    await cache.disconnect()
