"""
密码处理
使用bcrypt进行密码加密
"""

from passlib.context import CryptContext


class PasswordHandler:
    """密码处理器"""

    def __init__(self, schemes: list[str] = ["bcrypt"], deprecated: str = "auto"):
        self.pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)

    def hash(self, password: str) -> str:
        """
        加密密码

        Args:
            password: 明文密码

        Returns:
            加密后的密码哈希
        """
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码

        Args:
            plain_password: 明文密码
            hashed_password: 加密后的密码哈希

        Returns:
            密码是否匹配
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def needs_update(self, hashed_password: str) -> bool:
        """
        检查密码哈希是否需要更新

        Args:
            hashed_password: 加密后的密码哈希

        Returns:
            是否需要更新
        """
        return self.pwd_context.needs_update(hashed_password)


# 全局密码处理器实例
_password_handler = PasswordHandler()


def hash_password(password: str) -> str:
    """
    便捷函数:加密密码

    Args:
        password: 明文密码

    Returns:
        加密后的密码哈希
    """
    return _password_handler.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    便捷函数:验证密码

    Args:
        plain_password: 明文密码
        hashed_password: 加密后的密码哈希

    Returns:
        密码是否匹配
    """
    return _password_handler.verify(plain_password, hashed_password)
