from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel[T](BaseModel):
    """统一响应格式"""

    code: int = 200
    msg: str = "success"
    data: T | None = None

    @classmethod
    def success(cls, data: Any = None, msg: str = "success"):
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def error(cls, code: int = 500, msg: str = "error"):
        return cls(code=code, msg=msg, data=None)


class PageResult[T](BaseModel):
    """分页结果容器"""

    records: list[T]
    total: int
    current: int
    size: int
