"""
认证API路由
"""

import sys
from pathlib import Path
from fastapi import APIRouter, HTTPException, status, Depends

# 添加核心框架到路径
core_path = Path(__file__).parent.parent.parent.parent.parent / "core-framework"
sys.path.insert(0, str(core_path))

from auth.jwt_handler import get_jwt_handler
from auth.password import verify_password
from logging.logger import get_logger

from ..schemas.user import UserLogin, Token
from ..dependencies import get_database
from ..models.user import User

router = APIRouter()
logger = get_logger(__name__)


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db = Depends(get_database)):
    """
    用户登录

    - **username**: 用户名
    - **password**: 密码
    """
    logger.info("User login attempt", username=user_data.username)

    # 查询用户
    query = "SELECT * FROM users WHERE username = :username"
    user_dict = await db.fetch_one(query, {"username": user_data.username})

    if not user_dict:
        logger.warning("Login failed: user not found", username=user_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    # 验证密码
    if not verify_password(user_data.password, user_dict["hashed_password"]):
        logger.warning("Login failed: invalid password", username=user_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    # 检查用户是否激活
    if not user_dict["is_active"]:
        logger.warning("Login failed: user inactive", username=user_data.username)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    # 生成令牌
    jwt_handler = get_jwt_handler()
    access_token = jwt_handler.create_access_token(
        data={
            "sub": str(user_dict["id"]),
            "username": user_dict["username"],
            "email": user_dict["email"],
        }
    )
    refresh_token = jwt_handler.create_refresh_token(
        data={"sub": str(user_dict["id"])}
    )

    logger.info("User logged in successfully", user_id=user_dict["id"], username=user_data.username)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db = Depends(get_database)):
    """
    刷新访问令牌

    - **refresh_token**: 刷新令牌
    """
    jwt_handler = get_jwt_handler()

    # 验证刷新令牌
    payload = jwt_handler.verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
        )

    user_id = payload.get("sub")

    # 查询用户
    query = "SELECT * FROM users WHERE id = :id"
    user_dict = await db.fetch_one(query, {"id": int(user_id)})

    if not user_dict or not user_dict["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用",
        )

    # 生成新的访问令牌
    new_access_token = jwt_handler.create_access_token(
        data={
            "sub": str(user_dict["id"]),
            "username": user_dict["username"],
            "email": user_dict["email"],
        }
    )

    logger.info("Token refreshed", user_id=user_id)

    return Token(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout():
    """
    用户登出

    注意: 在实际应用中，应该将令牌加入黑名单
    """
    logger.info("User logged out")
    return {"message": "登出成功"}
