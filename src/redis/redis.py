import redis.asyncio as redis 
from src.schemas.setting import setting
import logging

JTI_EXPIRY = 3600


token_blocklist = redis.from_url(
    url=f"{setting.REDIS_URL}:{setting.REDIS_PORT}",
    decode_responses=True,
    db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    try: 
        await token_blocklist.set(
            name=jti,
            value="",
            ex=JTI_EXPIRY
        )
    except Exception as e:
        logging.warning("token blocklist redis not working")
        raise

async def token_in_blocklist(jti: str) -> bool:
    result = await token_blocklist.get(name=jti)
    return result is not None