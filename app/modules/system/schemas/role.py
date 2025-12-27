from pydantic import BaseModel, ConfigDict


class RoleOut(BaseModel):
    role_id: int
    name: str
    code: str

    model_config = ConfigDict(from_attributes=True)
