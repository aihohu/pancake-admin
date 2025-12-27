from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class LoginCredentials(BaseModel):
    """通用登录请求体 (适配 JSON)"""

    login_type: str = Field(
        "password", description="登录类型: password, sms, wechat, google"
    )
    user_name: str | None = None
    password: str | None = None
    mobile: str | None = None
    code: str | None = None  # 验证码
    token: str | None = None  # 第三方(WeChat/Google)授权码

    model_config = ConfigDict(
        alias_generator=to_camel,  # 自动将所有字段名转为驼峰作为别名
        populate_by_name=True,  # 允许通过字段名或别名进行初始化
    )


class RouteMeta(BaseModel):
    title: str
    icon: str | None = None
    localIcon: str | None = None
    order: int = 0
    requiresAuth: bool = True
    keepAlive: bool = False
    hideInMenu: bool = False
    activeMenu: str | None = None
    multiTab: bool = False


class UserRoute(BaseModel):
    name: str
    path: str
    component: str
    props: bool | None = None
    meta: RouteMeta
    children: list["UserRoute"] | None = None

    class Config:
        from_attributes = True
