"""
应用配置管理
基于Pydantic Settings
"""

from typing import Optional, List, Dict, Any
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """应用基础配置"""

    # 应用信息
    app_name: str = Field(default="Enterprise Platform", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    environment: str = Field(default="development", description="运行环境")
    debug: bool = Field(default=False, description="调试模式")

    # API配置
    api_prefix: str = Field(default="/api/v1", description="API前缀")
    allowed_hosts: List[str] = Field(default=["*"], description="允许的主机")
    cors_origins: List[str] = Field(default=["*"], description="CORS允许的源")

    # 服务配置
    host: str = Field(default="0.0.0.0", description="监听地址")
    port: int = Field(default=8000, description="监听端口")
    workers: int = Field(default=4, description="工作进程数")

    # 安全配置
    secret_key: str = Field(default="your-secret-key-here", description="密钥")
    access_token_expire_minutes: int = Field(default=30, description="访问令牌过期时间(分钟)")
    refresh_token_expire_days: int = Field(default=7, description="刷新令牌过期时间(天)")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="APP_",
    )


class DatabaseSettings(BaseSettings):
    """数据库配置"""

    # PostgreSQL配置
    postgres_host: str = Field(default="localhost", description="PostgreSQL主机")
    postgres_port: int = Field(default=5432, description="PostgreSQL端口")
    postgres_user: str = Field(default="postgres", description="PostgreSQL用户")
    postgres_password: str = Field(default="postgres", description="PostgreSQL密码")
    postgres_db: str = Field(default="enterprise_db", description="PostgreSQL数据库")

    # MySQL配置
    mysql_host: str = Field(default="localhost", description="MySQL主机")
    mysql_port: int = Field(default=3306, description="MySQL端口")
    mysql_user: str = Field(default="root", description="MySQL用户")
    mysql_password: str = Field(default="root", description="MySQL密码")
    mysql_db: str = Field(default="enterprise_db", description="MySQL数据库")

    # MongoDB配置
    mongodb_host: str = Field(default="localhost", description="MongoDB主机")
    mongodb_port: int = Field(default=27017, description="MongoDB端口")
    mongodb_user: str = Field(default="", description="MongoDB用户")
    mongodb_password: str = Field(default="", description="MongoDB密码")
    mongodb_db: str = Field(default="enterprise_db", description="MongoDB数据库")

    # 连接池配置
    pool_size: int = Field(default=10, description="连接池大小")
    max_overflow: int = Field(default=20, description="连接池最大溢出")
    pool_timeout: int = Field(default=30, description="连接池超时")
    pool_recycle: int = Field(default=3600, description="连接池回收时间")

    # SQLAlchemy配置
    echo_sql: bool = Field(default=False, description="是否打印SQL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="DB_",
    )

    @property
    def postgres_url(self) -> str:
        """PostgreSQL连接URL"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def mysql_url(self) -> str:
        """MySQL连接URL"""
        return (
            f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )

    @property
    def mongodb_url(self) -> str:
        """MongoDB连接URL"""
        auth = f"{self.mongodb_user}:{self.mongodb_password}@" if self.mongodb_user else ""
        return f"mongodb://{auth}{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db}"


class RedisSettings(BaseSettings):
    """Redis配置"""

    redis_host: str = Field(default="localhost", description="Redis主机")
    redis_port: int = Field(default=6379, description="Redis端口")
    redis_password: Optional[str] = Field(default=None, description="Redis密码")
    redis_db: int = Field(default=0, description="Redis数据库")
    redis_max_connections: int = Field(default=50, description="最大连接数")
    redis_socket_timeout: int = Field(default=5, description="Socket超时")
    redis_socket_connect_timeout: int = Field(default=5, description="连接超时")

    # Redis集群配置
    redis_cluster: bool = Field(default=False, description="是否使用集群")
    redis_cluster_nodes: List[str] = Field(default=[], description="集群节点")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="REDIS_",
    )

    @property
    def redis_url(self) -> str:
        """Redis连接URL"""
        password = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{password}{self.redis_host}:{self.redis_port}/{self.redis_db}"


class RabbitMQSettings(BaseSettings):
    """RabbitMQ配置"""

    rabbitmq_host: str = Field(default="localhost", description="RabbitMQ主机")
    rabbitmq_port: int = Field(default=5672, description="RabbitMQ端口")
    rabbitmq_user: str = Field(default="guest", description="RabbitMQ用户")
    rabbitmq_password: str = Field(default="guest", description="RabbitMQ密码")
    rabbitmq_vhost: str = Field(default="/", description="RabbitMQ虚拟主机")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="RABBITMQ_",
    )

    @property
    def rabbitmq_url(self) -> str:
        """RabbitMQ连接URL"""
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}{self.rabbitmq_vhost}"
        )


class LogSettings(BaseSettings):
    """日志配置"""

    log_level: str = Field(default="INFO", description="日志级别")
    log_file: Optional[str] = Field(default=None, description="日志文件")
    log_json_format: bool = Field(default=False, description="JSON格式")
    log_enable_colors: bool = Field(default=True, description="启用颜色")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="LOG_",
    )


class Settings(BaseSettings):
    """主配置类 - 整合所有配置"""

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)
    log: LogSettings = Field(default_factory=LogSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 自动加载子配置
        self.app = AppSettings()
        self.database = DatabaseSettings()
        self.redis = RedisSettings()
        self.rabbitmq = RabbitMQSettings()
        self.log = LogSettings()


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置实例(单例模式)

    Returns:
        Settings实例
    """
    return Settings()
