"""
RabbitMQ消息队列实现
"""

from typing import Optional
import asyncio
import uuid

import aio_pika
from aio_pika import Connection, Channel, Queue, Exchange, Message as AioPikaMessage
from aio_pika.abc import AbstractIncomingMessage

from .base import MessageQueueBase, MessageQueueConfig, Message, MessageHandler


class RabbitMQQueue(MessageQueueBase):
    """RabbitMQ消息队列实现"""

    def __init__(self, config: MessageQueueConfig):
        super().__init__(config)
        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None
        self._consumers = {}

    async def connect(self) -> None:
        """连接RabbitMQ"""
        if self._connected:
            return

        connection_url = (
            f"amqp://{self.config.username}:{self.config.password}@"
            f"{self.config.host}:{self.config.port}{self.config.virtual_host}"
        )

        self._connection = await aio_pika.connect_robust(
            connection_url,
            heartbeat=self.config.heartbeat,
            timeout=self.config.connection_timeout,
        )

        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=10)

        self._connected = True

    async def disconnect(self) -> None:
        """断开连接"""
        if not self._connected:
            return

        # 取消所有消费者
        for consumer_tag in list(self._consumers.keys()):
            await self._cancel_consumer(consumer_tag)

        if self._channel:
            await self._channel.close()
            self._channel = None

        if self._connection:
            await self._connection.close()
            self._connection = None

        self._connected = False

    async def publish(
        self,
        queue_name: str,
        message: Message,
        exchange: Optional[str] = None,
        routing_key: Optional[str] = None
    ) -> None:
        """发布消息"""
        if not self._connected or not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")

        # 设置消息ID
        if not message.message_id:
            message.message_id = str(uuid.uuid4())

        # 创建RabbitMQ消息
        rabbitmq_message = AioPikaMessage(
            body=message.serialize(),
            content_type=message.content_type,
            message_id=message.message_id,
            correlation_id=message.correlation_id,
            reply_to=message.reply_to,
            headers=message.headers,
            timestamp=message.timestamp,
        )

        if exchange:
            # 发布到交换机
            exch = await self._channel.get_exchange(exchange)
            await exch.publish(
                rabbitmq_message,
                routing_key=routing_key or queue_name
            )
        else:
            # 直接发布到队列
            await self._channel.default_exchange.publish(
                rabbitmq_message,
                routing_key=queue_name
            )

    async def consume(
        self,
        queue_name: str,
        callback: MessageHandler,
        auto_ack: bool = False
    ) -> None:
        """消费消息"""
        if not self._connected or not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")

        queue = await self._channel.get_queue(queue_name)

        async def on_message(incoming_message: AbstractIncomingMessage) -> None:
            try:
                # 反序列化消息
                message = Message.deserialize(incoming_message.body)
                message.message_id = incoming_message.message_id
                message.correlation_id = incoming_message.correlation_id
                message.reply_to = incoming_message.reply_to

                # 调用回调函数
                await callback(message)

                if not auto_ack:
                    await incoming_message.ack()

            except Exception as e:
                print(f"Error processing message: {e}")
                if not auto_ack:
                    await incoming_message.nack(requeue=True)

        consumer_tag = await queue.consume(on_message, no_ack=auto_ack)
        self._consumers[consumer_tag] = queue

    async def ack(self, delivery_tag: Any) -> None:
        """确认消息 (在RabbitMQ中通过message对象确认)"""
        # 在consume中已经处理
        pass

    async def nack(self, delivery_tag: Any, requeue: bool = True) -> None:
        """拒绝消息 (在RabbitMQ中通过message对象拒绝)"""
        # 在consume中已经处理
        pass

    async def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False
    ) -> Queue:
        """声明队列"""
        if not self._connected or not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")

        return await self._channel.declare_queue(
            queue_name,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete
        )

    async def delete_queue(self, queue_name: str) -> None:
        """删除队列"""
        if not self._connected or not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")

        queue = await self._channel.get_queue(queue_name)
        await queue.delete()

    async def purge_queue(self, queue_name: str) -> None:
        """清空队列"""
        if not self._connected or not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")

        queue = await self._channel.get_queue(queue_name)
        await queue.purge()

    async def declare_exchange(
        self,
        exchange_name: str,
        exchange_type: str = "direct",
        durable: bool = True,
        auto_delete: bool = False
    ) -> Exchange:
        """声明交换机"""
        if not self._connected or not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")

        return await self._channel.declare_exchange(
            exchange_name,
            type=exchange_type,
            durable=durable,
            auto_delete=auto_delete
        )

    async def bind_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str = ""
    ) -> None:
        """绑定队列到交换机"""
        if not self._connected or not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")

        queue = await self._channel.get_queue(queue_name)
        exchange = await self._channel.get_exchange(exchange_name)
        await queue.bind(exchange, routing_key=routing_key)

    async def _cancel_consumer(self, consumer_tag: str) -> None:
        """取消消费者"""
        if consumer_tag in self._consumers:
            queue = self._consumers[consumer_tag]
            await queue.cancel(consumer_tag)
            del self._consumers[consumer_tag]

    @property
    def channel(self) -> Channel:
        """获取通道"""
        if not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")
        return self._channel
