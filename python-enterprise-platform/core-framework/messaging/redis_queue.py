"""
Redis消息队列实现 (基于Redis List和Stream)
"""

from typing import Optional, Any
import asyncio
import uuid
import json

from redis.asyncio import Redis, ConnectionPool

from .base import MessageQueueBase, MessageQueueConfig, Message, MessageHandler


class RedisQueue(MessageQueueBase):
    """Redis消息队列实现"""

    def __init__(self, config: MessageQueueConfig, use_streams: bool = False):
        super().__init__(config)
        self._client: Optional[Redis] = None
        self._pool: Optional[ConnectionPool] = None
        self._consumers = {}
        self._consumer_tasks = {}
        self.use_streams = use_streams  # 使用Redis Streams还是List

    async def connect(self) -> None:
        """连接Redis"""
        if self._connected:
            return

        self._pool = ConnectionPool(
            host=self.config.host,
            port=self.config.port,
            password=self.config.password,
            db=self.config.db,
            decode_responses=False,
        )

        self._client = Redis(connection_pool=self._pool)
        await self._client.ping()

        self._connected = True

    async def disconnect(self) -> None:
        """断开连接"""
        if not self._connected:
            return

        # 停止所有消费者任务
        for task in self._consumer_tasks.values():
            task.cancel()

        if self._consumer_tasks:
            await asyncio.gather(*self._consumer_tasks.values(), return_exceptions=True)

        self._consumer_tasks.clear()
        self._consumers.clear()

        if self._client:
            await self._client.close()
            self._client = None

        if self._pool:
            await self._pool.disconnect()
            self._pool = None

        self._connected = False

    async def publish(
        self,
        queue_name: str,
        message: Message,
        exchange: Optional[str] = None,
        routing_key: Optional[str] = None
    ) -> None:
        """发布消息"""
        if not self._connected or not self._client:
            raise RuntimeError("Not connected to Redis")

        if not message.message_id:
            message.message_id = str(uuid.uuid4())

        serialized = message.serialize()

        if self.use_streams:
            # 使用Redis Streams
            await self._client.xadd(
                queue_name,
                {"data": serialized},
                maxlen=10000  # 限制stream长度
            )
        else:
            # 使用Redis List
            await self._client.rpush(queue_name, serialized)

    async def consume(
        self,
        queue_name: str,
        callback: MessageHandler,
        auto_ack: bool = False
    ) -> None:
        """消费消息"""
        if not self._connected or not self._client:
            raise RuntimeError("Not connected to Redis")

        consumer_id = str(uuid.uuid4())

        if self.use_streams:
            task = asyncio.create_task(
                self._consume_stream(queue_name, callback, consumer_id)
            )
        else:
            task = asyncio.create_task(
                self._consume_list(queue_name, callback, consumer_id)
            )

        self._consumer_tasks[consumer_id] = task
        self._consumers[consumer_id] = queue_name

    async def _consume_list(
        self,
        queue_name: str,
        callback: MessageHandler,
        consumer_id: str
    ) -> None:
        """从List消费消息"""
        while consumer_id in self._consumers:
            try:
                # 阻塞式弹出
                result = await self._client.blpop(queue_name, timeout=1)

                if result:
                    _, serialized = result
                    message = Message.deserialize(serialized)
                    await callback(message)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error consuming message: {e}")
                await asyncio.sleep(1)

    async def _consume_stream(
        self,
        queue_name: str,
        callback: MessageHandler,
        consumer_id: str
    ) -> None:
        """从Stream消费消息"""
        group_name = f"{queue_name}_group"

        # 创建消费者组
        try:
            await self._client.xgroup_create(
                queue_name,
                group_name,
                id="0",
                mkstream=True
            )
        except Exception:
            pass  # 组可能已存在

        last_id = ">"  # 读取新消息

        while consumer_id in self._consumers:
            try:
                # 从stream读取
                results = await self._client.xreadgroup(
                    group_name,
                    consumer_id,
                    {queue_name: last_id},
                    count=1,
                    block=1000
                )

                if results:
                    for stream_name, messages in results:
                        for msg_id, msg_data in messages:
                            serialized = msg_data.get(b"data")
                            if serialized:
                                message = Message.deserialize(serialized)
                                await callback(message)

                                # 确认消息
                                await self._client.xack(
                                    queue_name,
                                    group_name,
                                    msg_id
                                )

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error consuming message: {e}")
                await asyncio.sleep(1)

    async def ack(self, delivery_tag: Any) -> None:
        """确认消息 (在consume中已处理)"""
        pass

    async def nack(self, delivery_tag: Any, requeue: bool = True) -> None:
        """拒绝消息"""
        pass

    async def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False
    ) -> None:
        """声明队列 (Redis不需要显式声明)"""
        pass

    async def delete_queue(self, queue_name: str) -> None:
        """删除队列"""
        if not self._connected or not self._client:
            raise RuntimeError("Not connected to Redis")

        await self._client.delete(queue_name)

    async def purge_queue(self, queue_name: str) -> None:
        """清空队列"""
        await self.delete_queue(queue_name)

    async def queue_length(self, queue_name: str) -> int:
        """获取队列长度"""
        if not self._connected or not self._client:
            raise RuntimeError("Not connected to Redis")

        if self.use_streams:
            return await self._client.xlen(queue_name)
        else:
            return await self._client.llen(queue_name)

    @property
    def client(self) -> Redis:
        """获取Redis客户端"""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        return self._client
