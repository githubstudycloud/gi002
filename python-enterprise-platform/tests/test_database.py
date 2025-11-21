"""
数据库模块测试
"""

import pytest
import sys
from pathlib import Path

# 添加核心框架到路径
core_path = Path(__file__).parent.parent / "core-framework"
sys.path.insert(0, str(core_path))

from database import SQLDatabase, DatabaseConfig, DatabaseType


@pytest.mark.asyncio
async def test_sqlite_connection():
    """测试SQLite连接"""
    config = DatabaseConfig(
        type=DatabaseType.SQLITE,
        database="test.db"
    )

    db = SQLDatabase(config)

    # 连接数据库
    await db.connect()
    assert db.is_connected

    # 创建测试表
    await db.execute("""
        CREATE TABLE IF NOT EXISTS test_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # 插入数据
    await db.execute(
        "INSERT INTO test_users (username, email) VALUES (:username, :email)",
        {"username": "testuser", "email": "test@example.com"}
    )

    # 查询数据
    result = await db.fetch_one(
        "SELECT * FROM test_users WHERE username = :username",
        {"username": "testuser"}
    )

    assert result is not None
    assert result["username"] == "testuser"
    assert result["email"] == "test@example.com"

    # 查询所有数据
    results = await db.fetch_all("SELECT * FROM test_users")
    assert len(results) >= 1

    # 清理
    await db.execute("DROP TABLE test_users")
    await db.disconnect()
    assert not db.is_connected


@pytest.mark.asyncio
async def test_database_transaction():
    """测试数据库事务"""
    config = DatabaseConfig(
        type=DatabaseType.SQLITE,
        database="test_transaction.db"
    )

    db = SQLDatabase(config)
    await db.connect()

    # 创建表
    await db.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance INTEGER NOT NULL
        )
    """)

    # 使用事务
    async with db.transaction() as session:
        await session.execute(
            "INSERT INTO accounts (name, balance) VALUES ('Alice', 1000)"
        )
        await session.execute(
            "INSERT INTO accounts (name, balance) VALUES ('Bob', 500)"
        )

    # 验证数据
    results = await db.fetch_all("SELECT * FROM accounts")
    assert len(results) == 2

    # 清理
    await db.execute("DROP TABLE accounts")
    await db.disconnect()
