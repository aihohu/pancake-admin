from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_response import ResponseModel
from app.core.security import get_password_hash
from app.db.session import get_db
from app.modules.auth.schemas.auth import LoginCredentials
from app.modules.auth.service import auth_service, build_menu_tree, get_current_user
from app.modules.system.models.user import User
from app.modules.system.schemas.user import UserCreate, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut, summary="用户注册")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    注册新用户：校验重复 -> Hash密码 -> 持久化
    """
    # 1. 检查用户名是否已存在
    result = await db.execute(select(User).where(User.user_name == user_in.user_name))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="该用户名已被注册")

    # 2. 创建用户实例
    new_user = User(
        user_name=user_in.user_name,
        nickname=user_in.nickname,
        hashed_password=get_password_hash(user_in.password),  # 密码加密
        status="1",
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", summary="用户登录")
async def login(
    credentials: LoginCredentials,
    db: AsyncSession = Depends(get_db),
):
    result = await auth_service.authenticate(credentials, db)
    return result


# @router.post("/login", response_model=LoginResponse, summary="用户登录")
# async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
#     """
#     登录：验证身份 -> 签发 JWT
#     """
#     # 1. 查找用户
#     result = await db.execute(select(User).where(User.user_name == login_data.user_name))
#     user = result.scalars().first()

#     # 2. 验证密码
#     if not user or not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="账号或密码错误"
#         )

#     if not user.status:
#         raise HTTPException(status_code=403, detail="账号已被禁用")

#     # 3. 生成 Access Token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         subject=str(user.user_id), expires_delta=access_token_expires
#     )

#     return {
#         "token": {"access_token": access_token, "token_type": "Bearer"},
#         "user": user,
#     }


@router.get("/getUserInfo", summary="获取当前登录用户信息及权限")
async def get_user_info(current_user: User = Depends(get_current_user)):
    """
    获取用户信息
    """
    # 1. 提取角色编码列表 (如: ['admin', 'user'])
    roles = [role.role_code for role in current_user.roles]
    roles.append("R_SUPER")

    # 2. 提取按钮级权限标识 (如: ['sys:user:add', 'sys:user:edit'])
    # 遍历用户持有的所有角色，再遍历角色拥有的菜单，提取 permission 字段
    permissions = set()
    for role in current_user.roles:
        for menu in role.menus:
            if menu.permission:  # 只有定义了权限标识的才加入
                permissions.add(menu.permission)

    return ResponseModel.success(
        data={
            "userId": str(current_user.user_id),
            "userName": current_user.user_name,
            # "nickname": current_user.nickname,
            "roles": roles,
            "buttons": list(permissions),
        }
    )


@router.get("/getUserRoutes", summary="获取动态路由菜单")
async def get_user_routes(current_user: User = Depends(get_current_user)):
    """
    获取当前用户的动态路由树
    """
    # 1. 汇总当前用户所有角色下的菜单 (去重)
    all_menus_dict = {}
    for role in current_user.roles:
        for menu in role.menus:
            # 过滤掉按钮级权限，只保留菜单和目录 (假设类型 1是目录，2是菜单，3是按钮)
            if menu.menu_type in [1, 2]:
                all_menus_dict[menu.id] = menu

    # 2. 构建树形结构
    menu_list = list(all_menus_dict.values())
    route_tree = build_menu_tree(menu_list)

    return {"home": "dashboard_analysis", "routes": route_tree}  # 默认首页的路由 name
