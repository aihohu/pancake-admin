import redis.asyncio as redis

from app.core.config import settings

# 创建异步 Redis 实例
redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,  # 自动将返回结果转为字符串而非 bytes
)


async def get_redis():
    """供 FastAPI Depends 使用的依赖函数"""
    return redis_client
