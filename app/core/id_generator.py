from snowflake import SnowflakeGenerator

# 在实际生产中，worker_id 可以从环境变量或容器的主机名哈希中获取
# 这里默认设为 1
generator = SnowflakeGenerator(instance=1)


def next_id() -> int:
    """生成下一个雪花 ID"""
    return next(generator)
