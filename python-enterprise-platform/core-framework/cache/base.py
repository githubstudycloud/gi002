"""
缓存基类和配置
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, List
from enum import Enum


class CacheType(str, Enum):
    """缓存类型枚举"""
    REDIS = "redis"
    MEMCACHED = "memcached"
    MEMORY = "memory"


@dataclass
class CacheConfig:
    """缓存配置"""
    type: CacheType
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0
    max_connections: int = 50
    socket_timeout: int = 5
    socket_connect_timeout: int = 5
    decode_responses: bool = True

    # Redis集群配置
    cluster_mode: bool = False
    cluster_nodes: Optional[List[dict]] = None

    # 默认过期时间(秒)
    default_ttl: int = 3600

    def __post_init__(self) -> None:
        if self.cluster_nodes is None:
            self.cluster_nodes = []


class CacheBase(ABC):
    """缓存基类 - 定义统一接口"""

    def __init__(self, config: CacheConfig):
        self.config = config
        self._connected = False

    @abstractmethod
    async def connect(self) -> None:
        """连接缓存服务器"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """断开缓存连接"""
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        pass

    @abstractmethod
    async def expire(self, key: str, ttl: int) -> bool:
        """设置过期时间"""
        pass

    @abstractmethod
    async def ttl(self, key: str) -> int:
        """获取键的剩余生存时间"""
        pass

    @abstractmethod
    async def keys(self, pattern: str = "*") -> List[str]:
        """获取匹配的键列表"""
        pass

    @abstractmethod
    async def flush(self) -> bool:
        """清空所有缓存"""
        pass

    @abstractmethod
    async def incr(self, key: str, amount: int = 1) -> int:
        """递增"""
        pass

    @abstractmethod
    async def decr(self, key: str, amount: int = 1) -> int:
        """递减"""
        pass

    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._connected

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.disconnect()
