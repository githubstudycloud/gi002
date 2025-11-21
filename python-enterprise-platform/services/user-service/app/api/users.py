"""
用户管理API路由
"""

import sys
from pathlib import Path
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
import json

# 添加核心框架到路径
core_path = Path(__file__).parent.parent.parent.parent.parent / "core-framework"
sys.path.insert(0, str(core_path))

from auth.password import hash_password
from logging.logger import get_logger

from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..dependencies import get_database, get_cache

router = APIRouter()
logger = get_logger(__name__)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db = Depends(get_database)):
    """
    创建新用户

    - **username**: 用户名 (3-50字符)
    - **email**: 邮箱地址
    - **password**: 密码 (最少8字符)
    - **full_name**: 全名 (可选)
    - **roles**: 角色列表 (默认为["user"])
    """
    logger.info("Creating new user", username=user.username, email=user.email)

    # 检查用户名是否存在
    existing = await db.fetch_one(
        "SELECT id FROM users WHERE username = :username",
        {"username": user.username}
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )

    # 检查邮箱是否存在
    existing = await db.fetch_one(
        "SELECT id FROM users WHERE email = :email",
        {"email": user.email}
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="邮箱已被使用"
        )

    # 加密密码
    hashed_password = hash_password(user.password)

    # 插入用户
    query = """
        INSERT INTO users (username, email, hashed_password, full_name, roles)
        VALUES (:username, :email, :hashed_password, :full_name, :roles)
        RETURNING id, username, email, full_name, is_active, is_superuser, roles, created_at
    """

    result = await db.fetch_one(query, {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "full_name": user.full_name,
        "roles": json.dumps(user.roles),
    })

    logger.info("User created successfully", user_id=result["id"], username=user.username)

    return UserResponse(
        id=result["id"],
        username=result["username"],
        email=result["email"],
        full_name=result["full_name"],
        is_active=result["is_active"],
        is_superuser=result["is_superuser"],
        roles=json.loads(result["roles"]) if result["roles"] else [],
        created_at=result["created_at"],
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db = Depends(get_database), cache = Depends(get_cache)):
    """
    获取用户信息

    - **user_id**: 用户ID
    """
    # 尝试从缓存获取
    cache_key = f"user:{user_id}"
    cached_data = await cache.get(cache_key)

    if cached_data:
        logger.info("User data retrieved from cache", user_id=user_id)
        return UserResponse(**json.loads(cached_data))

    # 从数据库查询
    query = "SELECT * FROM users WHERE id = :id"
    user_dict = await db.fetch_one(query, {"id": user_id})

    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    user_response = UserResponse(
        id=user_dict["id"],
        username=user_dict["username"],
        email=user_dict["email"],
        full_name=user_dict["full_name"],
        is_active=user_dict["is_active"],
        is_superuser=user_dict["is_superuser"],
        roles=json.loads(user_dict["roles"]) if user_dict["roles"] else [],
        created_at=user_dict["created_at"],
    )

    # 缓存用户数据
    await cache.set(cache_key, json.dumps(user_response.model_dump(), default=str), ttl=300)

    logger.info("User data retrieved from database", user_id=user_id)
    return user_response


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_database)
):
    """
    获取用户列表

    - **skip**: 跳过记录数
    - **limit**: 返回记录数限制
    """
    query = "SELECT * FROM users ORDER BY created_at DESC LIMIT :limit OFFSET :skip"
    users = await db.fetch_all(query, {"limit": limit, "skip": skip})

    return [
        UserResponse(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            is_active=user["is_active"],
            is_superuser=user["is_superuser"],
            roles=json.loads(user["roles"]) if user["roles"] else [],
            created_at=user["created_at"],
        )
        for user in users
    ]


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db = Depends(get_database),
    cache = Depends(get_cache)
):
    """
    更新用户信息

    - **user_id**: 用户ID
    """
    # 检查用户是否存在
    existing = await db.fetch_one("SELECT id FROM users WHERE id = :id", {"id": user_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 构建更新语句
    update_data = {}
    if user_update.email is not None:
        update_data["email"] = user_update.email
    if user_update.full_name is not None:
        update_data["full_name"] = user_update.full_name
    if user_update.password is not None:
        update_data["hashed_password"] = hash_password(user_update.password)
    if user_update.is_active is not None:
        update_data["is_active"] = user_update.is_active
    if user_update.roles is not None:
        update_data["roles"] = json.dumps(user_update.roles)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="没有需要更新的数据"
        )

    # 构建SQL语句
    set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    query = f"""
        UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
        RETURNING id, username, email, full_name, is_active, is_superuser, roles, created_at
    """

    update_data["id"] = user_id
    result = await db.fetch_one(query, update_data)

    # 清除缓存
    cache_key = f"user:{user_id}"
    await cache.delete(cache_key)

    logger.info("User updated successfully", user_id=user_id)

    return UserResponse(
        id=result["id"],
        username=result["username"],
        email=result["email"],
        full_name=result["full_name"],
        is_active=result["is_active"],
        is_superuser=result["is_superuser"],
        roles=json.loads(result["roles"]) if result["roles"] else [],
        created_at=result["created_at"],
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db = Depends(get_database),
    cache = Depends(get_cache)
):
    """
    删除用户

    - **user_id**: 用户ID
    """
    # 检查用户是否存在
    existing = await db.fetch_one("SELECT id FROM users WHERE id = :id", {"id": user_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 删除用户
    await db.execute("DELETE FROM users WHERE id = :id", {"id": user_id})

    # 清除缓存
    cache_key = f"user:{user_id}"
    await cache.delete(cache_key)

    logger.info("User deleted successfully", user_id=user_id)
