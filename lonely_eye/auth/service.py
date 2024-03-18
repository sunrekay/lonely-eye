import uuid
from typing import Any

from redis.asyncio import Redis

from lonely_eye.auth import utils, exceptions
from lonely_eye.config import settings


async def login(
    model: Any,
    client: Redis,
    key_generator_func,
):
    refresh_token_id = str(uuid.uuid4())
    saved: bool = await client.set(
        name=key_generator_func(
            model.id,
            model.username,
        ),
        value=refresh_token_id,
        ex=settings.redis.refresh_token_expire_seconds,
    )

    if not saved:
        raise exceptions.problem_with_redis_connection

    return utils.tokens_info(
        model=model,
        refresh_token_id=refresh_token_id,
    )


async def refresh(
    model: Any,
    client: Redis,
    key_generator_func,
):
    refresh_token_id = str(uuid.uuid4())
    deleted = await client.delete(
        key_generator_func(
            model.id,
            model.username,
        )
    )
    if not deleted:
        raise exceptions.refresh_token_invalid
    return utils.tokens_info(
        model=model,
        refresh_token_id=refresh_token_id,
    )


async def logout(
    model: Any,
    client: Redis,
    key_generator_func,
):
    await client.delete(
        key_generator_func(
            model.id,
            model.username,
        )
    )
