import json
from datetime import date, datetime
from app.services.rate_limit import redis_client

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

async def get_cached_json(key: str):
    """Retrieves and parses JSON from Redis."""
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception:
        pass
    return None

from fastapi.encoders import jsonable_encoder

async def set_cached_json(key: str, data: any, ttl: int = 3600):
    """Serializes and stores data in Redis."""
    try:
        serialized = jsonable_encoder(data)
        json_str = json.dumps(serialized, cls=CustomJSONEncoder)
        await redis_client.setex(key, ttl, json_str)
    except Exception as e:
        print(f"Redis cache set error: {e}")

async def clear_cache_namespace(namespace: str):
    """Clears all keys under a specific namespace prefix."""
    try:
        keys = await redis_client.keys(f"{namespace}:*")
        if keys:
            await redis_client.delete(*keys)
    except Exception:
        pass
