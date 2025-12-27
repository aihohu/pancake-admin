from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic.alias_generators import to_camel


class UserBase(BaseModel):
    user_name: str = Field(..., min_length=4, max_length=50, description="账号")
    nickname: str | None = Field(None, max_length=50, description="昵称")

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="明文密码")


class UserLogin(BaseModel):
    user_name: str = Field(..., description="账号")
    password: str = Field(..., description="密码")


class UserQuery(BaseModel):
    """用户查询参数"""

    current: int = 1
    size: int = 10
    user_name: str | None = None
    nickname: str | None = None
    status: bool | None = None  # 是否激活

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class UserOut(UserBase):
    user_id: int
    is_active: bool

    # 核心：返回给前端时转为字符串
    @field_serializer("user_id")
    def serialize_id(self, user_id: int, _info):
        return str(user_id)

    # 核心：允许 Pydantic 直接读取 SQLAlchemy 模型属性
    model_config = ConfigDict(from_attributes=True)


class UserItemOut(BaseModel):
    """列表显示的用户对象"""

    user_id: int
    user_name: str
    nickname: str | None = None
    is_active: bool
    create_time: datetime
    # 可以在此扩展角色信息
    roles: list[str] = []

    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel, populate_by_name=True
    )

    # 核心：处理 Snowflake ID 精度丢失问题
    @field_serializer("user_id")
    def serialize_id(self, user_id: int, _info):
        return str(user_id)
