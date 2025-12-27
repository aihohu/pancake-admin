from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings  # 假设你在 core/config.py 中处理了环境变量

# 1. 创建异步数据库引擎
# echo=True 会在终端打印 SQL 语句，开发环境下很有用
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # 自动检查连接是否存活
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 超过池大小后允许的额外连接数
)

# 2. 创建异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # 异步环境下通常设为 False 避免属性过期错误
)


# 3. 定义声明式基类（供 models 使用）
class Base(DeclarativeBase):
    pass


# 4. 数据库依赖注入函数 (Dependency Injection)
# 这个函数用于 FastAPI 的 Depends()
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    每个请求创建一个新的异步 Session，并在请求结束时自动关闭。
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # 也可以在业务代码中手动 commit
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
