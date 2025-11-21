"""
MongoDB数据库实现
使用Motor异步驱动
"""

from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from .base import DatabaseBase, DatabaseConfig


class MongoDBDatabase(DatabaseBase):
    """MongoDB数据库实现"""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None

    async def connect(self) -> None:
        """连接MongoDB"""
        if self._connected:
            return

        connection_string = self.config.get_connection_string()

        self._client = AsyncIOMotorClient(
            connection_string,
            maxPoolSize=self.config.pool_size,
            **self.config.options,
        )

        self._database = self._client[self.config.database]
        self._connected = True

        # 测试连接
        await self._client.admin.command('ping')

    async def disconnect(self) -> None:
        """断开MongoDB连接"""
        if not self._connected:
            return

        if self._client:
            self._client.close()
            self._client = None

        self._database = None
        self._connected = False

    async def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """执行MongoDB命令"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        # MongoDB不使用SQL，这里提供命令执行接口
        return await self._database.command(query, **(params or {}))

    async def fetch_one(
        self,
        collection: str,
        filter_query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """查询单条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        result = await coll.find_one(filter_query or {}, projection)

        # 转换ObjectId为字符串
        if result and '_id' in result:
            result['_id'] = str(result['_id'])

        return result

    async def fetch_all(
        self,
        collection: str,
        filter_query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 0,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """查询多条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        cursor = coll.find(filter_query or {}, projection)

        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        if sort:
            cursor = cursor.sort(sort)

        results = await cursor.to_list(length=limit if limit else None)

        # 转换ObjectId为字符串
        for result in results:
            if '_id' in result:
                result['_id'] = str(result['_id'])

        return results

    async def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        """插入单条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        result = await coll.insert_one(document)
        return str(result.inserted_id)

    async def insert_many(self, collection: str, documents: List[Dict[str, Any]]) -> List[str]:
        """插入多条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        result = await coll.insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    async def update_one(
        self,
        collection: str,
        filter_query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> int:
        """更新单条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        result = await coll.update_one(filter_query, update, upsert=upsert)
        return result.modified_count

    async def update_many(
        self,
        collection: str,
        filter_query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> int:
        """更新多条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        result = await coll.update_many(filter_query, update, upsert=upsert)
        return result.modified_count

    async def delete_one(self, collection: str, filter_query: Dict[str, Any]) -> int:
        """删除单条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        result = await coll.delete_one(filter_query)
        return result.deleted_count

    async def delete_many(self, collection: str, filter_query: Dict[str, Any]) -> int:
        """删除多条文档"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        result = await coll.delete_many(filter_query)
        return result.deleted_count

    async def count_documents(self, collection: str, filter_query: Optional[Dict[str, Any]] = None) -> int:
        """统计文档数量"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")

        coll = self._database[collection]
        return await coll.count_documents(filter_query or {})

    @asynccontextmanager
    async def transaction(self):
        """MongoDB事务上下文管理器"""
        if not self._connected or not self._client:
            raise RuntimeError("Database not connected")

        async with await self._client.start_session() as session:
            async with session.start_transaction():
                yield session

    def get_collection(self, name: str) -> AsyncIOMotorCollection:
        """获取集合"""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected")
        return self._database[name]

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """获取数据库对象"""
        if not self._database:
            raise RuntimeError("Database not connected")
        return self._database

    @property
    def client(self) -> AsyncIOMotorClient:
        """获取客户端"""
        if not self._client:
            raise RuntimeError("Database not connected")
        return self._client
