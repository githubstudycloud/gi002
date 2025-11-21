"""
消息队列基类和配置
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Callable, Awaitable
from enum import Enum
import json
from datetime import datetime


class QueueType(str, Enum):
    """消息队列类型"""
    RABBITMQ = "rabbitmq"
    KAFKA = "kafka"
    REDIS = "redis"


@dataclass
class Message:
    """消息对象"""
    body: Any
    headers: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    message_id: Optional[str] = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    content_type: str = "application/json"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "body": self.body,
            "headers": self.headers,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
            "correlation_id": self.correlation_id,
            "reply_to": self.reply_to,
            "content_type": self.content_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """从字典创建"""
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            body=data.get("body"),
            headers=data.get("headers", {}),
            timestamp=timestamp or datetime.utcnow(),
            message_id=data.get("message_id"),
            correlation_id=data.get("correlation_id"),
            reply_to=data.get("reply_to"),
            content_type=data.get("content_type", "application/json"),
        )

    def serialize(self) -> bytes:
        """序列化消息"""
        return json.dumps(self.to_dict()).encode()

    @classmethod
    def deserialize(cls, data: bytes) -> "Message":
        """反序列化消息"""
        return cls.from_dict(json.loads(data.decode()))


@dataclass
class MessageQueueConfig:
    """消息队列配置"""
    type: QueueType
    host: str = "localhost"
    port: int = 5672
    username: str = "guest"
    password: str = "guest"
    virtual_host: str = "/"

    # 连接配置
    heartbeat: int = 60
    connection_timeout: int = 30

    # Kafka特定配置
    group_id: Optional[str] = None
    auto_offset_reset: str = "earliest"

    # Redis特定配置
    db: int = 0


MessageHandler = Callable[[Message], Awaitable[None]]


class MessageQueueBase(ABC):
    """消息队列基类"""

    def __init__(self, config: MessageQueueConfig):
        self.config = config
        self._connected = False

    @abstractmethod
    async def connect(self) -> None:
        """连接消息队列"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """断开连接"""
        pass

    @abstractmethod
    async def publish(
        self,
        queue_name: str,
        message: Message,
        exchange: Optional[str] = None,
        routing_key: Optional[str] = None
    ) -> None:
        """发布消息"""
        pass

    @abstractmethod
    async def consume(
        self,
        queue_name: str,
        callback: MessageHandler,
        auto_ack: bool = False
    ) -> None:
        """消费消息"""
        pass

    @abstractmethod
    async def ack(self, delivery_tag: Any) -> None:
        """确认消息"""
        pass

    @abstractmethod
    async def nack(self, delivery_tag: Any, requeue: bool = True) -> None:
        """拒绝消息"""
        pass

    @abstractmethod
    async def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False
    ) -> None:
        """声明队列"""
        pass

    @abstractmethod
    async def delete_queue(self, queue_name: str) -> None:
        """删除队列"""
        pass

    @abstractmethod
    async def purge_queue(self, queue_name: str) -> None:
        """清空队列"""
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
