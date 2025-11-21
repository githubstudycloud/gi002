"""
SQL数据库实现 (PostgreSQL, MySQL, SQLite)
使用SQLAlchemy异步引擎
"""

from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import text, MetaData
from sqlalchemy.orm import DeclarativeBase

from .base import DatabaseBase, DatabaseConfig


class Base(DeclarativeBase):
    """SQLAlchemy声明式基类"""
    metadata = MetaData()


class SQLDatabase(DatabaseBase):
    """SQL数据库实现"""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    async def connect(self) -> None:
        """连接数据库"""
        if self._connected:
            return

        connection_string = self.config.get_connection_string()

        self._engine = create_async_engine(
            connection_string,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow,
            pool_timeout=self.config.pool_timeout,
            pool_recycle=self.config.pool_recycle,
            echo=self.config.echo,
            **self.config.options,
        )

        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        self._connected = True

    async def disconnect(self) -> None:
        """断开数据库连接"""
        if not self._connected:
            return

        if self._engine:
            await self._engine.dispose()
            self._engine = None

        self._session_factory = None
        self._connected = False

    async def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """执行SQL语句"""
        if not self._connected:
            raise RuntimeError("Database not connected")

        async with self.get_session() as session:
            result = await session.execute(text(query), params or {})
            await session.commit()
            return result

    async def fetch_one(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """查询单条记录"""
        if not self._connected:
            raise RuntimeError("Database not connected")

        async with self.get_session() as session:
            result = await session.execute(text(query), params or {})
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

    async def fetch_all(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """查询多条记录"""
        if not self._connected:
            raise RuntimeError("Database not connected")

        async with self.get_session() as session:
            result = await session.execute(text(query), params or {})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]

    @asynccontextmanager
    async def transaction(self):
        """事务上下文管理器"""
        if not self._connected:
            raise RuntimeError("Database not connected")

        async with self.get_session() as session:
            async with session.begin():
                yield session

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """获取数据库会话"""
        if not self._session_factory:
            raise RuntimeError("Database not connected")

        async with self._session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_tables(self, base: Optional[DeclarativeBase] = None) -> None:
        """创建所有表"""
        if not self._connected:
            raise RuntimeError("Database not connected")

        target_base = base or Base
        async with self._engine.begin() as conn:
            await conn.run_sync(target_base.metadata.create_all)

    async def drop_tables(self, base: Optional[DeclarativeBase] = None) -> None:
        """删除所有表"""
        if not self._connected:
            raise RuntimeError("Database not connected")

        target_base = base or Base
        async with self._engine.begin() as conn:
            await conn.run_sync(target_base.metadata.drop_all)

    @property
    def engine(self) -> AsyncEngine:
        """获取引擎"""
        if not self._engine:
            raise RuntimeError("Database not connected")
        return self._engine
