from fastapi import Depends, HTTPException

from app.modules.auth.service import get_current_user
from app.modules.system.models.user import User


def check_permissions(required_perm: str):
    """
    权限检查装饰器工厂

    用法:
        @router.get("/data", dependencies=[Depends(check_permissions("sys:user:list"))])
    """

    async def permission_dependency(current_user: User = Depends(get_current_user)):
        # 汇总当前用户所有权限
        user_perms = {
            m.permission for r in current_user.roles for m in r.menus if m.permission
        }

        # 如果不是超级管理员且没有所需权限
        if (
            "admin" not in [r.code for r in current_user.roles]
            and required_perm not in user_perms
        ):
            raise HTTPException(status_code=403, detail=f"缺少权限: {required_perm}")
        return True

    return permission_dependency
