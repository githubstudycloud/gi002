"""
基于角色的访问控制 (RBAC)
"""

from typing import Set, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class Permission(str, Enum):
    """权限枚举"""
    # 用户权限
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

    # 角色权限
    ROLE_CREATE = "role:create"
    ROLE_READ = "role:read"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"

    # 订单权限
    ORDER_CREATE = "order:create"
    ORDER_READ = "order:read"
    ORDER_UPDATE = "order:update"
    ORDER_DELETE = "order:delete"
    ORDER_APPROVE = "order:approve"

    # 系统权限
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_CONFIG = "system:config"
    SYSTEM_MONITOR = "system:monitor"


@dataclass
class Role:
    """角色"""
    name: str
    description: str
    permissions: Set[Permission] = field(default_factory=set)
    parent_roles: Set[str] = field(default_factory=set)

    def has_permission(self, permission: Permission) -> bool:
        """检查是否拥有指定权限"""
        return permission in self.permissions

    def add_permission(self, permission: Permission) -> None:
        """添加权限"""
        self.permissions.add(permission)

    def remove_permission(self, permission: Permission) -> None:
        """移除权限"""
        self.permissions.discard(permission)

    def add_permissions(self, permissions: List[Permission]) -> None:
        """批量添加权限"""
        self.permissions.update(permissions)


class RBACManager:
    """RBAC管理器"""

    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self._initialize_default_roles()

    def _initialize_default_roles(self) -> None:
        """初始化默认角色"""
        # 超级管理员
        admin_role = Role(
            name="admin",
            description="系统管理员",
            permissions={
                Permission.SYSTEM_ADMIN,
                Permission.SYSTEM_CONFIG,
                Permission.SYSTEM_MONITOR,
                Permission.USER_CREATE,
                Permission.USER_READ,
                Permission.USER_UPDATE,
                Permission.USER_DELETE,
                Permission.ROLE_CREATE,
                Permission.ROLE_READ,
                Permission.ROLE_UPDATE,
                Permission.ROLE_DELETE,
                Permission.ORDER_CREATE,
                Permission.ORDER_READ,
                Permission.ORDER_UPDATE,
                Permission.ORDER_DELETE,
                Permission.ORDER_APPROVE,
            }
        )

        # 普通用户
        user_role = Role(
            name="user",
            description="普通用户",
            permissions={
                Permission.USER_READ,
                Permission.ORDER_CREATE,
                Permission.ORDER_READ,
            }
        )

        # 订单管理员
        order_manager_role = Role(
            name="order_manager",
            description="订单管理员",
            permissions={
                Permission.ORDER_CREATE,
                Permission.ORDER_READ,
                Permission.ORDER_UPDATE,
                Permission.ORDER_DELETE,
                Permission.ORDER_APPROVE,
            },
            parent_roles={"user"}
        )

        # 用户管理员
        user_manager_role = Role(
            name="user_manager",
            description="用户管理员",
            permissions={
                Permission.USER_CREATE,
                Permission.USER_READ,
                Permission.USER_UPDATE,
                Permission.USER_DELETE,
            },
            parent_roles={"user"}
        )

        self.roles["admin"] = admin_role
        self.roles["user"] = user_role
        self.roles["order_manager"] = order_manager_role
        self.roles["user_manager"] = user_manager_role

    def create_role(
        self,
        name: str,
        description: str,
        permissions: Optional[List[Permission]] = None,
        parent_roles: Optional[List[str]] = None
    ) -> Role:
        """
        创建角色

        Args:
            name: 角色名称
            description: 角色描述
            permissions: 权限列表
            parent_roles: 父角色列表

        Returns:
            创建的角色
        """
        role = Role(
            name=name,
            description=description,
            permissions=set(permissions or []),
            parent_roles=set(parent_roles or [])
        )
        self.roles[name] = role
        return role

    def get_role(self, name: str) -> Optional[Role]:
        """获取角色"""
        return self.roles.get(name)

    def delete_role(self, name: str) -> bool:
        """删除角色"""
        if name in self.roles:
            del self.roles[name]
            return True
        return False

    def get_all_permissions(self, role_name: str) -> Set[Permission]:
        """
        获取角色的所有权限(包括继承的权限)

        Args:
            role_name: 角色名称

        Returns:
            权限集合
        """
        role = self.roles.get(role_name)
        if not role:
            return set()

        permissions = role.permissions.copy()

        # 递归获取父角色的权限
        for parent_role_name in role.parent_roles:
            parent_permissions = self.get_all_permissions(parent_role_name)
            permissions.update(parent_permissions)

        return permissions

    def has_permission(self, role_name: str, permission: Permission) -> bool:
        """
        检查角色是否拥有指定权限

        Args:
            role_name: 角色名称
            permission: 权限

        Returns:
            是否拥有权限
        """
        permissions = self.get_all_permissions(role_name)
        return permission in permissions

    def has_any_permission(self, role_name: str, permissions: List[Permission]) -> bool:
        """
        检查角色是否拥有任意一个权限

        Args:
            role_name: 角色名称
            permissions: 权限列表

        Returns:
            是否拥有任意权限
        """
        role_permissions = self.get_all_permissions(role_name)
        return any(p in role_permissions for p in permissions)

    def has_all_permissions(self, role_name: str, permissions: List[Permission]) -> bool:
        """
        检查角色是否拥有所有权限

        Args:
            role_name: 角色名称
            permissions: 权限列表

        Returns:
            是否拥有所有权限
        """
        role_permissions = self.get_all_permissions(role_name)
        return all(p in role_permissions for p in permissions)

    def user_has_permission(self, user_roles: List[str], permission: Permission) -> bool:
        """
        检查用户是否拥有指定权限

        Args:
            user_roles: 用户角色列表
            permission: 权限

        Returns:
            是否拥有权限
        """
        for role_name in user_roles:
            if self.has_permission(role_name, permission):
                return True
        return False

    def user_has_any_permission(self, user_roles: List[str], permissions: List[Permission]) -> bool:
        """
        检查用户是否拥有任意一个权限

        Args:
            user_roles: 用户角色列表
            permissions: 权限列表

        Returns:
            是否拥有任意权限
        """
        for role_name in user_roles:
            if self.has_any_permission(role_name, permissions):
                return True
        return False

    def user_has_all_permissions(self, user_roles: List[str], permissions: List[Permission]) -> bool:
        """
        检查用户是否拥有所有权限

        Args:
            user_roles: 用户角色列表
            permissions: 权限列表

        Returns:
            是否拥有所有权限
        """
        all_user_permissions = set()
        for role_name in user_roles:
            all_user_permissions.update(self.get_all_permissions(role_name))

        return all(p in all_user_permissions for p in permissions)


# 全局RBAC管理器实例
_rbac_manager = RBACManager()


def get_rbac_manager() -> RBACManager:
    """获取全局RBAC管理器"""
    return _rbac_manager
