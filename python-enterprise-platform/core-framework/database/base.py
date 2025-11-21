"""
数据库基类和配置
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type
from enum import Enum


class DatabaseType(str, Enum):
    """数据库类型枚举"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"


@dataclass
class DatabaseConfig:
    """数据库配置"""
    type: DatabaseType
    host: str = "localhost"
    port: int = 5432
    username: str = ""
    password: str = ""
    database: str = ""
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False

    # MongoDB特定配置
    replica_set: Optional[str] = None
    auth_source: str = "admin"

    # 额外选项
    options: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.options is None:
            self.options = {}

    def get_connection_string(self) -> str:
        """获取数据库连接字符串"""
        if self.type == DatabaseType.MONGODB:
            auth = f"{self.username}:{self.password}@" if self.username else ""
            replica = f"?replicaSet={self.replica_set}" if self.replica_set else ""
            return f"mongodb://{auth}{self.host}:{self.port}/{self.database}{replica}"

        elif self.type in [DatabaseType.POSTGRESQL, DatabaseType.MYSQL]:
            driver = "postgresql+asyncpg" if self.type == DatabaseType.POSTGRESQL else "mysql+aiomysql"
            auth = f"{self.username}:{self.password}@" if self.username else ""
            return f"{driver}://{auth}{self.host}:{self.port}/{self.database}"

        elif self.type == DatabaseType.SQLITE:
            return f"sqlite+aiosqlite:///{self.database}"

        raise ValueError(f"Unsupported database type: {self.type}")


class DatabaseBase(ABC):
    """数据库基类 - 定义统一接口"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._connected = False

    @abstractmethod
    async def connect(self) -> None:
        """连接数据库"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """断开数据库连接"""
        pass

    @abstractmethod
    async def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """执行SQL/查询语句"""
        pass

    @abstractmethod
    async def fetch_one(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """查询单条记录"""
        pass

    @abstractmethod
    async def fetch_all(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """查询多条记录"""
        pass

    @abstractmethod
    async def transaction(self):
        """开始事务"""
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
