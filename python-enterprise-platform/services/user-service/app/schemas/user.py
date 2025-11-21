"""
用户数据Schema (Pydantic模型)
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """用户基础Schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """创建用户Schema"""
    password: str = Field(..., min_length=8, max_length=100)
    roles: List[str] = Field(default_factory=lambda: ["user"])


class UserUpdate(BaseModel):
    """更新用户Schema"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None


class UserInDB(UserBase):
    """数据库中的用户Schema"""
    id: int
    is_active: bool
    is_superuser: bool
    roles: List[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    """用户响应Schema"""
    id: int
    is_active: bool
    is_superuser: bool
    roles: List[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """用户登录Schema"""
    username: str
    password: str


class Token(BaseModel):
    """令牌Schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据Schema"""
    user_id: str
    username: Optional[str] = None
    scopes: List[str] = []
