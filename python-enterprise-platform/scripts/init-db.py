"""
数据库初始化脚本
创建所有必要的表
"""

import asyncio
import sys
from pathlib import Path

# 添加路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "core-framework"))
sys.path.insert(0, str(project_root / "services" / "user-service"))

from database import SQLDatabase, DatabaseConfig, DatabaseType
from config.settings import get_settings


async def create_user_table(db: SQLDatabase):
    """创建用户表"""
    print("创建用户表...")

    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE NOT NULL,
            is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
            roles TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """)

    # 创建索引
    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)
    """)

    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
    """)

    print("✅ 用户表创建完成")


async def create_default_admin(db: SQLDatabase):
    """创建默认管理员账户"""
    from auth.password import hash_password
    import json

    print("创建默认管理员账户...")

    # 检查是否已存在
    existing = await db.fetch_one(
        "SELECT id FROM users WHERE username = :username",
        {"username": "admin"}
    )

    if existing:
        print("⚠️  管理员账户已存在，跳过创建")
        return

    # 创建管理员
    hashed_password = hash_password("Admin123456!")

    await db.execute("""
        INSERT INTO users (username, email, hashed_password, full_name, is_superuser, roles)
        VALUES (:username, :email, :hashed_password, :full_name, :is_superuser, :roles)
    """, {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": hashed_password,
        "full_name": "系统管理员",
        "is_superuser": True,
        "roles": json.dumps(["admin"])
    })

    print("✅ 管理员账户创建完成")
    print("   用户名: admin")
    print("   密码:   Admin123456!")


async def main():
    """主函数"""
    print("=" * 60)
    print("  数据库初始化")
    print("=" * 60)
    print()

    # 获取配置
    settings = get_settings()

    # 创建数据库配置
    config = DatabaseConfig(
        type=DatabaseType.POSTGRESQL,
        host=settings.database.postgres_host,
        port=settings.database.postgres_port,
        username=settings.database.postgres_user,
        password=settings.database.postgres_password,
        database=settings.database.postgres_db,
    )

    # 连接数据库
    db = SQLDatabase(config)

    try:
        print("连接数据库...")
        await db.connect()
        print("✅ 数据库连接成功")
        print()

        # 创建表
        await create_user_table(db)
        print()

        # 创建默认管理员
        await create_default_admin(db)
        print()

        print("=" * 60)
        print("  ✅ 数据库初始化完成！")
        print("=" * 60)

    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
