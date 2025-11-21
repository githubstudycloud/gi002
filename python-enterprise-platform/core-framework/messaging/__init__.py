"""
消息队列抽象层
支持: RabbitMQ, Kafka, Redis Stream
"""

from .base import MessageQueueBase, MessageQueueConfig, Message
from .rabbitmq_queue import RabbitMQQueue
from .redis_queue import RedisQueue

__all__ = [
    "MessageQueueBase",
    "MessageQueueConfig",
    "Message",
    "RabbitMQQueue",
    "RedisQueue",
]
