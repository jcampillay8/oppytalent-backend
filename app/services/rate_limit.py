import time
import redis.asyncio as redis
from fastapi import HTTPException, status

from app.config import settings

# Initialize Redis client
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

async def check_rate_limit(ip_address: str, max_requests: int = 5, window_seconds: int = 60):
    """
    Limita la cantidad de peticiones permitidas por IP.
    Permite `max_requests` por cada `window_seconds`.
    """
    key = f"rate_limit:chat:{ip_address}"
    current_time = time.time()
    
    try:
        async with redis_client.pipeline(transaction=True) as pipe:
            # Remove timestamps older than the window
            pipe.zremrangebyscore(key, 0, current_time - window_seconds)
            # Add the current timestamp. Value needs to be unique, so we use time + index or just exact time float
            pipe.zadd(key, {str(current_time): current_time})
            # Count the number of requests in the window
            pipe.zcard(key)
            # Set the expiration of the key
            pipe.expire(key, window_seconds)
            
            results = await pipe.execute()
            request_count = results[2]
            
        if request_count > max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Se ha excedido el límite de consultas al chat. Por favor, intenta en un minuto."
            )
    except redis.RedisError:
        # Fallback if Redis is down: pass through to avoid breaking the chat
        pass

async def get_moderation_strikes(ip_address: str) -> int:
    key = f"moderation_strikes:{ip_address}"
    try:
        strikes = await redis_client.get(key)
        return int(strikes) if strikes else 0
    except redis.RedisError:
        return 0

async def add_moderation_strike(ip_address: str) -> int:
    key = f"moderation_strikes:{ip_address}"
    try:
        strikes = await redis_client.incr(key)
        if strikes == 1:
            # Expire strikes after 24 hours (86400 seconds)
            await redis_client.expire(key, 86400)
        return strikes
    except redis.RedisError:
        return 0
