from pydantic import BaseModel

from app.modules.system.schemas.user import UserOut


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class LoginResponse(BaseModel):
    token: Token
    user: UserOut  # 包含用户信息
