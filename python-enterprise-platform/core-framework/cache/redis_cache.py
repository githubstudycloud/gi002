"""
Redis缓存实现
"""

from typing import Any, Optional, List
import json
import pickle

from redis.asyncio import Redis, ConnectionPool
from redis.asyncio.cluster import RedisCluster

from .base import CacheBase, CacheConfig


class RedisCache(CacheBase):
    """Redis缓存实现"""

    def __init__(self, config: CacheConfig, serializer: str = "json"):
        super().__init__(config)
        self._client: Optional[Redis] = None
        self._pool: Optional[ConnectionPool] = None
        self.serializer = serializer  # json or pickle

    async def connect(self) -> None:
        """连接Redis"""
        if self._connected:
            return

        if self.config.cluster_mode:
            # 集群模式
            self._client = RedisCluster(
                startup_nodes=self.config.cluster_nodes,
                decode_responses=self.config.decode_responses,
                password=self.config.password,
            )
        else:
            # 单机模式
            self._pool = ConnectionPool(
                host=self.config.host,
                port=self.config.port,
                password=self.config.password,
                db=self.config.db,
                max_connections=self.config.max_connections,
                socket_timeout=self.config.socket_timeout,
                socket_connect_timeout=self.config.socket_connect_timeout,
                decode_responses=self.config.decode_responses,
            )
            self._client = Redis(connection_pool=self._pool)

        # 测试连接
        await self._client.ping()
        self._connected = True

    async def disconnect(self) -> None:
        """断开Redis连接"""
        if not self._connected:
            return

        if self._client:
            await self._client.close()
            self._client = None

        if self._pool:
            await self._pool.disconnect()
            self._pool = None

        self._connected = False

    def _serialize(self, value: Any) -> str:
        """序列化值"""
        if self.serializer == "pickle":
            return pickle.dumps(value)
        else:
            return json.dumps(value)

    def _deserialize(self, value: str) -> Any:
        """反序列化值"""
        if not value:
            return None

        if self.serializer == "pickle":
            return pickle.loads(value)
        else:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value

    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        value = await self._client.get(key)
        return self._deserialize(value) if value else None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        serialized = self._serialize(value)
        expire_time = ttl if ttl is not None else self.config.default_ttl

        if expire_time:
            return await self._client.setex(key, expire_time, serialized)
        else:
            return await self._client.set(key, serialized)

    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        result = await self._client.delete(key)
        return result > 0

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        result = await self._client.exists(key)
        return result > 0

    async def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        return await self._client.expire(key, ttl)

    async def ttl(self, key: str) -> int:
        """获取键的剩余生存时间"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        return await self._client.ttl(key)

    async def keys(self, pattern: str = "*") -> List[str]:
        """获取匹配的键列表"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        keys = await self._client.keys(pattern)
        return [key.decode() if isinstance(key, bytes) else key for key in keys]

    async def flush(self) -> bool:
        """清空所有缓存"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        return await self._client.flushdb()

    async def incr(self, key: str, amount: int = 1) -> int:
        """递增"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        return await self._client.incrby(key, amount)

    async def decr(self, key: str, amount: int = 1) -> int:
        """递减"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        return await self._client.decrby(key, amount)

    # Redis特有方法

    async def hget(self, name: str, key: str) -> Optional[Any]:
        """从哈希表获取值"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        value = await self._client.hget(name, key)
        return self._deserialize(value) if value else None

    async def hset(self, name: str, key: str, value: Any) -> int:
        """设置哈希表值"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        serialized = self._serialize(value)
        return await self._client.hset(name, key, serialized)

    async def hgetall(self, name: str) -> dict:
        """获取哈希表所有键值对"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        result = await self._client.hgetall(name)
        return {k.decode() if isinstance(k, bytes) else k: self._deserialize(v)
                for k, v in result.items()}

    async def lpush(self, key: str, *values: Any) -> int:
        """从列表左侧推入"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        serialized = [self._serialize(v) for v in values]
        return await self._client.lpush(key, *serialized)

    async def rpush(self, key: str, *values: Any) -> int:
        """从列表右侧推入"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        serialized = [self._serialize(v) for v in values]
        return await self._client.rpush(key, *serialized)

    async def lpop(self, key: str) -> Optional[Any]:
        """从列表左侧弹出"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        value = await self._client.lpop(key)
        return self._deserialize(value) if value else None

    async def rpop(self, key: str) -> Optional[Any]:
        """从列表右侧弹出"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        value = await self._client.rpop(key)
        return self._deserialize(value) if value else None

    async def lrange(self, key: str, start: int, end: int) -> List[Any]:
        """获取列表范围"""
        if not self._connected or not self._client:
            raise RuntimeError("Cache not connected")

        values = await self._client.lrange(key, start, end)
        return [self._deserialize(v) for v in values]

    @property
    def client(self) -> Redis:
        """获取Redis客户端"""
        if not self._client:
            raise RuntimeError("Cache not connected")
        return self._client
