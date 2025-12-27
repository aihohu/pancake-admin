from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.base_response import ResponseModel


def setup_exception_handlers(app: FastAPI):
    # 1. 捕获所有未知的系统异常
    @app.exception_handler(Exception)
    async def all_exception_handler(_request: Request, _exc: Exception):
        # 这里可以加入日志记录
        return JSONResponse(
            status_code=500,
            content=ResponseModel.error(message="服务器内部错误").model_dump(),
        )

    # 2. 捕获 Pydantic 参数校验错误 (422 错误)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ):
        # 提取具体的错误字段和原因
        errors = exc.errors()
        msg = f"参数错误: {errors[0]['loc'][-1]} {errors[0]['msg']}"
        return JSONResponse(
            status_code=422,
            content=ResponseModel.error(code=422, message=msg).model_dump(),
        )
