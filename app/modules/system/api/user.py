from fastapi import APIRouter, Depends
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import get_current_user
from app.core.base_response import PageResult, ResponseModel
from app.db.session import get_db
from app.modules.system.models.user import User
from app.modules.system.schemas.user import UserItemOut, UserQuery

router = APIRouter()


@router.get(
    "/list", response_model=ResponseModel[PageResult[UserItemOut]], summary="用户列表"
)
async def get_user_list(
    query: UserQuery = Depends(),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    # 1. 构建查询条件
    filters = []
    if query.user_name:
        filters.append(User.user_name.contains(query.user_name))
    if query.nickname:
        filters.append(User.nickname.contains(query.nickname))
    if query.status is not None:
        filters.append(User.is_active == query.status)

    # 2. 查询总数
    count_stmt = select(func.count()).select_from(User).where(and_(*filters))
    total = (await db.execute(count_stmt)).scalar() or 0

    # 3. 分页查询数据
    # 使用 selectinload 预加载角色信息
    stmt = (
        select(User)
        .where(and_(*filters))
        .offset((query.current - 1) * query.size)
        .limit(query.size)
        .options(selectinload(User.roles))
        .order_by(User.create_time.desc())
    )
    result = await db.execute(stmt)
    users = result.scalars().all()

    # 4. 转换为 Schema 对象 (处理角色简化)
    user_list = []
    for u in users:
        item = UserItemOut.model_validate(u)
        item.roles = [r.name for r in u.roles]
        user_list.append(item)

    # 5. 返回分页包装结果
    page_data = PageResult(
        records=user_list, total=total, current=query.current, size=query.size
    )
    return ResponseModel.success(data=page_data)
