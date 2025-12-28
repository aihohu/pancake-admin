from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from pydantic.alias_generators import to_camel

from app.utils.mask_util import MaskUtil


class UserBase(BaseModel):
    user_name: str = Field(..., min_length=4, max_length=50, description="账号")
    nickname: str | None = Field(None, max_length=50, description="昵称")
    user_email: str = Field(..., description="邮箱")
    user_phone: str = Field(..., description="手机号")
    user_gender: str = Field(..., description="用户性别")
    is_active: str = Field(..., description="状态")
    roles: list[str] = []  # 创建时分配的角色 ID 列表

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class UserCreate(UserBase):
    password: str | None = Field(..., min_length=6, description="明文密码")


class UserUpdate(UserBase):
    password: str | None = Field(..., min_length=6, description="明文密码")


class UserLogin(BaseModel):
    user_name: str = Field(..., description="账号")
    password: str = Field(..., description="密码")


class UserQuery(BaseModel):
    """用户查询参数"""

    current: int = 1
    size: int = 10
    user_name: str | None = None
    nickname: str | None = None
    status: bool | None = None

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class UserOut(BaseModel):
    user_id: int
    user_name: str
    nickname: str
    is_active: str

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
    user_email: str | None = None
    user_phone: str | None = None
    user_gender: str | None = None
    is_active: str | None = None
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

    @field_serializer("user_phone")
    def serialize_phone(self, v: str) -> str:
        return MaskUtil.phone(v)

    @field_serializer("user_email")
    def serialize_email(self, v: str) -> str:
        return MaskUtil.email(v)

    @field_serializer("create_time")
    def serialize_create_time(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @field_validator("roles", mode="before")
    @classmethod
    def transform_roles(cls, v):
        # 如果传入的是 SQLAlchemy 的 Role 对象列表，则提取名称
        if v and not isinstance(v[0], str):
            return [r.role_name for r in v]
        return v
