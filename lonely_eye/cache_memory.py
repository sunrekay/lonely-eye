from redis.asyncio import ConnectionPool, Redis

from lonely_eye.config import settings


class Keys:
    @staticmethod
    def worker_refresh_token(_id, username):
        return f"worker:refresh_token:{_id}:{username}"

    @staticmethod
    def manager_refresh_token(_id, username):
        return f"manager:refresh_token:{_id}:{username}"

    @staticmethod
    def worker_photo_url(_id, username):
        return f"manager:photo_url:{_id}:{username}"


class CacheMemory:
    def __init__(self, host: str, port: int):
        self.pool = ConnectionPool(
            host=host,
            port=port,
            **{"decode_responses": True},
        )

    def pool_dependency(self) -> Redis:
        return Redis(connection_pool=self.pool)


cache_memory = CacheMemory(
    host=settings.redis.host,
    port=settings.redis.port,
)
