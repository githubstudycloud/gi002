"""
JWT令牌处理
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from pydantic import BaseModel


class TokenData(BaseModel):
    """令牌数据"""
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    scopes: list[str] = []


class JWTHandler:
    """JWT处理器"""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        创建访问令牌

        Args:
            data: 要编码的数据
            expires_delta: 过期时间增量

        Returns:
            JWT令牌字符串
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        创建刷新令牌

        Args:
            data: 要编码的数据
            expires_delta: 过期时间增量

        Returns:
            JWT令牌字符串
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """
        验证令牌

        Args:
            token: JWT令牌
            token_type: 令牌类型 (access 或 refresh)

        Returns:
            解码后的数据,如果验证失败返回None
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # 验证令牌类型
            if payload.get("type") != token_type:
                return None

            # 验证过期时间
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                return None

            return payload

        except JWTError:
            return None

    def decode_token(self, token: str) -> Optional[TokenData]:
        """
        解码令牌为TokenData对象

        Args:
            token: JWT令牌

        Returns:
            TokenData对象,如果解码失败返回None
        """
        payload = self.verify_token(token)
        if not payload:
            return None

        try:
            return TokenData(
                user_id=payload.get("sub", ""),
                username=payload.get("username"),
                email=payload.get("email"),
                scopes=payload.get("scopes", []),
            )
        except Exception:
            return None


# 全局实例(需要在应用启动时初始化)
_jwt_handler: Optional[JWTHandler] = None


def initialize_jwt_handler(
    secret_key: str,
    algorithm: str = "HS256",
    access_token_expire_minutes: int = 30,
    refresh_token_expire_days: int = 7,
) -> None:
    """初始化全局JWT处理器"""
    global _jwt_handler
    _jwt_handler = JWTHandler(
        secret_key=secret_key,
        algorithm=algorithm,
        access_token_expire_minutes=access_token_expire_minutes,
        refresh_token_expire_days=refresh_token_expire_days,
    )


def get_jwt_handler() -> JWTHandler:
    """获取全局JWT处理器"""
    if _jwt_handler is None:
        raise RuntimeError("JWT handler not initialized. Call initialize_jwt_handler first.")
    return _jwt_handler


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """便捷函数:创建访问令牌"""
    return get_jwt_handler().create_access_token(data, expires_delta)


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """便捷函数:验证令牌"""
    return get_jwt_handler().verify_token(token, token_type)
